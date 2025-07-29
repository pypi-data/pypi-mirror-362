# SPDX-License-Identifier: MIT
# Authors: Benjamin Dodge
from collections import namedtuple
from typing import Any, Callable

import jax
import jax.numpy as jnp
from jax import lax
from jax.tree_util import Partial
from jax import Array

try:
    import jaxkd_cuda  # type: ignore

    global_has_cuda = True
except ImportError:
    global_has_cuda = False

__all__ = [
    "build_tree",
    "query_neighbors",
    "count_neighbors",
]

# These functions handle batching, are automatically JIT-compiled, and do a few sanity checks.
# If you need to run the non-JIT version, use `_build_tree`, `_single_query_neighbors`,
# and `_single_count_neighbors` instead. Both neighbor functions are implemented using a call
# to `_traverse_tree` with a custom `update_func` that tracks state.

tree_type = namedtuple("Tree", ["points", "indices", "split_dims"])


@Partial(jax.jit, static_argnames=("k", "optimize", "cuda"))
def build_and_query(
    points: Array, query: Array, *, k: int, optimize: bool = True, cuda: bool = False
) -> tuple[Array, Array]:
    """
    Build a k-d tree from points find the k nearest neighbors of queries.
    This is a convenience function that combines `build_tree` and `query_neighbors`.
    If multiple queries are needed for the same points, it is more efficient to call `build_tree` once and then `query_neighbors` multiple times.

    Args:
        points: (N, d) Points to build the tree from.
        query: (d,) or (Q, d) Query point(s).
        k (int): Number of neighbors to return.
        optimize: If True (default), split along dimension with the largest range. If False, cycle through dimensions in order.
        cuda: If False (default), use pure JAX. If True, use the jaxkd-cuda extension for faster tree construction. Requires the extension to be installed and `optimize=True`.

    Returns:
        neighbors: (k,) or (Q, k) Indices of the k nearest neighbors of query point(s).
        distances: (k,) or (Q, k) Distances to the k nearest neighbors of query point(s).
    """
    tree = build_tree(points, optimize=optimize, cuda=cuda)
    return query_neighbors(tree, query, k=k, cuda=cuda)


@Partial(jax.jit, static_argnames=("optimize", "cuda"))
def build_tree(points: Array, optimize: bool = True, cuda: bool = False) -> tree_type:
    """
    Build a k-d tree from points.

    Construction algorithm from Wald (2023), https://arxiv.org/abs/2211.00120.
    See also https://github.com/ingowald/cudaKDTree.

    Args:
        points: (N, d)
        optimize: If True (default), split along dimension with the largest range. This typically leads to faster queries. If False, cycle through dimensions in order.
        cuda: If False (default), use pure JAX. If True, use the jaxkd-cuda extension for faster tree construction. Requires the extension to be installed and `optimize=True`.

    Returns:
        tree (tree_type)
            - points: (N, d) Same points as input, not copied.
            - indices: (N,) Indices of points in binary tree order.
            - split_dims: (N,) Splitting dimension of each tree node, marked -1 for leaves. If `optimize=False` this is set to None.
    """
    if points.ndim != 2:
        raise ValueError(f"Points must have shape (N, d). Got shape {points.shape}.")
    if points.shape[-1] >= 128:
        raise ValueError(f"Maximum dimension 127, got {points.shape[-1]} dimensions.")
    if jax.config.jax_enable_x64 is False and len(points) > 2**31 - 1:  # type: ignore
        raise ValueError(
            f"len(points)={len(points)} exceeds maximum value of int32 for indices, try 64-bit mode (in future might also have uint32 option)"
        )
    if not cuda:
        return _build_tree(points, optimize=optimize)
    else:
        if not global_has_cuda:
            raise ImportError("jaxkd-cuda extension is not installed")
        if not optimize:
            raise ValueError("jaxkd-cuda extension requires optimize=True")
        points, indices, split_dims = jaxkd_cuda.build_tree(points)
        return tree_type(points, indices, split_dims)


@Partial(jax.jit, static_argnames=("k", "cuda"))
def query_neighbors(
    tree: tree_type, query: Array, *, k: int, cuda: bool = False
) -> tuple[Array, Array]:
    """
    Find the k nearest neighbors in a k-d tree.

    Traversal algorithm from Wald (2022), https://arxiv.org/abs/2210.12859.
    See also https://github.com/ingowald/cudaKDTree.

    Args:
        tree (tree_type): Output of `build_tree`.
            - points: (N, d) Points to search.
            - indices: (N,) Indices of points in binary tree order.
            - split_dims: (N,) Splitting dimension of each tree node, not used for leaves. If None, assume cycle through dimensions in order.
        query: (d,) or (Q, d) Query point(s).
        k (int): Number of neighbors to return.
        cuda: If False (default), use pure JAX. If True, use the jaxkd-cuda extension for faster tree construction. Requires the extension to be installed and `optimize=True`.

    Returns:
        neighbors: (k,) or (Q, k) Indices of the k nearest neighbors of query point(s).
        distances: (k,) or (Q, k) Distances to the k nearest neighbors of query point(s).
    """
    _check_tree(tree)
    if k > len(tree.points):
        raise ValueError(f"Queried {k} neighbors but tree contains only {len(tree.points)} points.")

    query_shaped = jnp.atleast_2d(query)

    if not cuda:
        neighbors, distances = jax.vmap(lambda q: _single_query_neighbors(tree, q, k=k))(
            query_shaped
        )
    else:
        if not global_has_cuda:
            raise ImportError("jaxkd-cuda extension is not installed")
        if tree.split_dims is None:
            raise ValueError("jaxkd-cuda extension requires optimize=True, i.e. split_dims=None")
        neighbors, distances = jaxkd_cuda.query_neighbors(
            (tree.points, tree.indices, tree.split_dims), query_shaped, k=k
        )

    if query.ndim == 1:
        return jnp.squeeze(neighbors, axis=0), jnp.squeeze(distances, axis=0)
    if query.ndim == 2:
        return neighbors, distances
    raise ValueError(f"Query must have shape (Q, d) or (d,). Got shape {query.shape}.")


@Partial(jax.jit, static_argnames=("cuda",))
def count_neighbors(
    tree: tree_type, query: Array, *, r: float | Array, cuda: bool = False
) -> Array:
    """
    Count the neighbors inside a given radius in a k-d tree.

    Traversal algorithm from Wald (2022), https://arxiv.org/abs/2210.12859.
    See also https://github.com/ingowald/cudaKDTree.

    Args:
        tree (tree_type): Output of `build_tree`.
            - points: (N, d) Points to search.
            - indices: (N,) Indices of points in binary tree order.
            - split_dims: (N,) Splitting dimension of each tree node, not used for leaves. If None, assume cycle through dimensions in order.
        query: (d,) or (Q, d) Query point(s).
        r: (float) (R,) or (Q, R) Radius or radii to count neighbors within, multiple radii are done in a single tree traversal.
        cuda: If False (default), use pure JAX. If True, use the jaxkd-cuda extension for faster tree construction. Requires the extension to be installed and `optimize=True`.

    Returns:
        counts: (int) (Q,) (R,) or (Q, R) Number of neighbors within the given radius(i) of query point(s).
    """
    _check_tree(tree)
    r = jnp.asarray(r)
    if (
        r.ndim > 2
        or query.ndim > 2
        or (r.ndim == 2 and query.ndim == 1)
        or ((r.ndim == 2 and query.ndim == 2) and r.shape[0] != query.shape[0])
    ):
        raise ValueError(f"Invalid shape for query {query.shape} or radius {r.shape}.")

    query_shaped = jnp.atleast_2d(query)
    r_shaped = jnp.atleast_2d(r)
    r_shaped = jnp.broadcast_to(r_shaped, (query_shaped.shape[0], r_shaped.shape[-1]))

    if not cuda:
        counts = jax.vmap(lambda q, r: _single_count_neighbors(tree, q, r=r))(
            query_shaped, r_shaped
        )
    else:
        if not global_has_cuda:
            raise ImportError("jaxkd-cuda extension is not installed")
        if tree.split_dims is None:
            raise ValueError("jaxkd-cuda extension requires optimize=True, i.e. split_dims=None")
        counts = jaxkd_cuda.count_neighbors(
            (tree.points, tree.indices, tree.split_dims), query_shaped, r_shaped
        )

    if r.ndim == 0:
        counts = jnp.squeeze(counts, axis=1)
    if query.ndim == 1:
        counts = jnp.squeeze(counts, axis=0)
    return counts


def _check_tree(tree: tree_type) -> None:
    """Check if the tree is valid."""
    points, indices, split_dims = tree.points, tree.indices, tree.split_dims
    if len(points) != len(indices):
        raise ValueError(f"Invalid tree, {len(points)} points and {len(indices)} indices.")
    if split_dims is not None and len(split_dims) != len(points):
        raise ValueError(f"Invalid tree, {len(points)} points and {len(split_dims)} split dims.")
    if jax.config.jax_enable_x64 is False and len(points) > 2**32 - 1:  # type: ignore
        raise ValueError(f"len(points)={len(points)} exceeds maximum value of int32, try int64")


def _single_query_neighbors(tree: tree_type, query: Array, *, k: int) -> tuple[Array, Array]:
    """Single neighbor query implementation, use `query_neighbors` wrapper instead unless non-JIT version is needed."""
    points, indices = tree.points, tree.indices

    def update_func(node, state, _):
        neighbors, square_distances = state
        # square distance to node point
        square_distance = jnp.sum(jnp.square(query - points[indices[node]]), axis=-1)
        max_neighbor = jnp.argmax(square_distances)
        neighbors, square_distances = lax.cond(
            # if the node is closer than the farthest neighbor, replace
            square_distance < square_distances[max_neighbor],
            lambda _: (
                neighbors.at[max_neighbor].set(indices[node]),
                square_distances.at[max_neighbor].set(square_distance),
            ),
            lambda _: (neighbors, square_distances),
            None,
        )
        return (neighbors, square_distances), jnp.max(square_distances)

    neighbors = -1 * jnp.ones(k, dtype=indices.dtype)
    square_distances = jnp.inf * jnp.ones(k, dtype=points.dtype)
    neighbors, _ = _traverse_tree(
        tree, query, update_func, (neighbors, square_distances), jnp.asarray(jnp.inf)
    )
    # recompute distances to enable VJP
    distances = jnp.linalg.norm(points[neighbors] - query, axis=-1)
    # sort primarily by distance, and secondarily by index for well-defined order
    distances, neighbors = lax.sort((distances, neighbors), dimension=0, num_keys=2)
    return neighbors, distances


def _single_count_neighbors(tree: tree_type, query: Array, *, r: float | Array) -> Array:
    """Single neighbor count implementation, use `count_neighbors` wrapper instead unless non-JIT version is needed."""
    r = jnp.asarray(r)
    points, indices = tree.points, tree.indices

    def update_func(node, count, square_radius):
        # square distance to node point
        square_distance = jnp.sum(jnp.square(query - points[indices[node]]), axis=-1)
        # if the node is within radius, increment count
        count = lax.select(square_distance < jnp.square(r), count + 1, count)
        return count, square_radius

    count = jnp.zeros(len(r), dtype=indices.dtype)
    count = _traverse_tree(tree, query, update_func, count, jnp.max(jnp.square(r)))
    return count


def _build_tree(points: Array, optimize: bool = True) -> tree_type:
    """
    Base k-d tree construction logic https://arxiv.org/abs/2211.00120.

    Can be used as a non-JIT version of `build_tree`, although rarely worth it.
    """
    n_points = len(points)
    n_levels = n_points.bit_length()
    array_index = jnp.arange(n_points, dtype=int)  # needed at various points

    def step(carry, level):
        nodes, indices, split_dims = carry

        # Compute split dimension and extract values along that dimension
        if optimize:
            dim_max = jax.ops.segment_max(points[indices], nodes, num_segments=n_points)
            dim_min = jax.ops.segment_min(points[indices], nodes, num_segments=n_points)
            new_split_dims = jnp.asarray(jnp.argmax(dim_max - dim_min, axis=-1), dtype=jnp.int8)
            split_dims = jnp.where(array_index < (1 << level) - 1, split_dims, new_split_dims)
            points_along_dim = jnp.squeeze(
                jnp.take_along_axis(points[indices], split_dims[nodes][:, jnp.newaxis], axis=-1),
                axis=-1,
            )
        else:
            split_dim = jnp.asarray(jnp.mod(level, points.shape[-1]), dtype=jnp.int8)
            points_along_dim = points[indices][:, split_dim]

        # Sort the points in each node segment along the splitting dimension
        nodes, _, indices = lax.sort((nodes, points_along_dim, indices), dimension=0, num_keys=2)

        # Compute the segment start index
        height = n_levels - level - 1
        n_left_siblings = nodes - ((1 << level) - 1)  # nodes to the left at the same level
        branch_start = (
            ((1 << level) - 1)  # levels above
            + n_left_siblings * ((1 << height) - 1)  # left sibling internal descendants
            + jnp.minimum(n_left_siblings * (1 << height), n_points - ((1 << (n_levels - 1)) - 1))
            # left sibling leaf descendants
        )

        # Compute the size of the left child segment
        left_child = 2 * nodes + 1
        child_height = jnp.maximum(0, height - 1)
        # first leaf of the left child, cryptic but just descends 2i+1 several times
        first_left_leaf = ~((~left_child) << child_height)
        left_branch_size = (
            ((1 << child_height) - 1)  # internal nodes
            + jnp.minimum(1 << child_height, jnp.maximum(0, n_points - first_left_leaf))
            # leaf nodes
        )

        # Split segment about the pivot
        pivot_position = branch_start + left_branch_size
        right_child = 2 * nodes + 2
        nodes = lax.select(
            # if node is pivot or in upper part of tree, keep it
            (array_index == pivot_position) | (array_index < (1 << level) - 1),
            nodes,
            # otherwise, put as left or right child
            lax.select(array_index < pivot_position, left_child, right_child),
        )

        return (nodes, indices, split_dims), None

    # Start all points at root and sort into tree at each level
    nodes = jnp.zeros(n_points, dtype=int)
    indices = jnp.arange(n_points, dtype=int)
    # technically the last few might be leaves if not a complete tree, but that's fine
    split_dims = -1 * jnp.ones(n_points, dtype=jnp.int8) if optimize else None
    # nodes should equal jnp.arange(n_points) at the end
    (nodes, indices, split_dims), _ = lax.scan(
        step, (nodes, indices, split_dims), jnp.arange(n_levels)
    )
    if isinstance(split_dims, Array):
        split_dims = split_dims.at[n_points // 2 :].set(-1)  # mark leaves as -1
    return tree_type(points, indices, split_dims)


def _traverse_tree(
    tree: tree_type,
    query: Array,
    update_func: Callable[[Array, Any, Array], tuple[Any, Array]],
    initial_state: Any,
    initial_square_radius: Array,
):
    """
    Base k-d tree traversal logic https://arxiv.org/abs/2210.12859.

    At each node, we run:
        `state, square_radius = update_func(node, state, square_radius)`
    """
    points, indices, split_dims = tree.points, tree.indices, tree.split_dims
    n_points = len(points)

    def step(carry):
        # Update neighbors with the current node if necessary
        current, previous, state, square_radius = carry
        parent = (current - 1) // 2
        state, square_radius = lax.cond(
            previous == parent, update_func, lambda _, s, r: (s, r), current, state, square_radius
        )

        # Locate children and determine if far child is in range
        level = jnp.frexp(current + 1)[1] - 1  # robust way top compute floor(log2(current + 1))
        split_dim = jnp.mod(level, points.shape[-1]) if split_dims is None else split_dims[current]
        split_distance = query[split_dim] - points[indices[current], split_dim]
        near_side = jnp.asarray(split_distance > 0, dtype=indices.dtype)
        near_child = 2 * current + 1 + near_side
        far_child = 2 * current + 2 - near_side
        far_in_range = jnp.square(split_distance) <= square_radius

        # Determine next node to traverse
        next = lax.select(
            # go to the far child if we came from near child or near child doesn't exist
            (previous == near_child) | ((previous == parent) & (near_child >= n_points)),
            # only go to the far child if it exists and is in range
            lax.select((far_child < n_points) & far_in_range, far_child, parent),
            # go to the near child if it exists and we came from the parent
            lax.select(previous == parent, near_child, parent),
        )
        return next, current, state, square_radius

    # Loop until we return to root
    current = jnp.asarray(0, dtype=indices.dtype)
    previous = (current - 1) // 2
    _, _, state, _ = lax.while_loop(
        lambda carry: carry[0] != (current - 1) // 2,
        step,
        (current, previous, initial_state, initial_square_radius),
    )
    return state
