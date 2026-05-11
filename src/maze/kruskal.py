"""
Randomized Kruskal's algorithm for maze generation.

Steps:
1. List all potential edges and shuffle them.
2. For each edge, if the two cells belong to different components,
   remove the wall and merge components (UnionFind).

Yields snapshots of (r1,c1,r2,c2) as each wall is removed so the
visualizer can animate the construction step by step.
"""

import random
from src.maze.grid import Grid, UnionFind


def kruskal(grid: Grid, seed: int | None = None):
    """
    Generate a perfect maze using randomized Kruskal.

    Args:
        grid: an empty Grid (no passages open).
        seed: random seed for reproducibility.

    Yields:
        (r1, c1, r2, c2) each time a wall is removed.
    """
    rng = random.Random(seed)

    rows, cols = grid.rows, grid.cols
    edges = list(grid.all_edges())
    rng.shuffle(edges)

    uf = UnionFind(rows * cols)

    def cell_id(r: int, c: int) -> int:
        return r * cols + c

    for r1, c1, r2, c2 in edges:
        a, b = cell_id(r1, c1), cell_id(r2, c2)
        if uf.union(a, b):
            grid.remove_wall(r1, c1, r2, c2)
            yield r1, c1, r2, c2


def generate_kruskal(rows: int, cols: int, seed: int | None = None):
    """Convenience: build a complete maze and return (grid, steps)."""
    grid = Grid(rows, cols)
    steps = list(kruskal(grid, seed=seed))
    return grid, steps
