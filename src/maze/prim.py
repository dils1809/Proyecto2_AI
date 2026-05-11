"""
Randomized Prim's algorithm for maze generation.

Steps:
1. Start from a random cell; mark it visited.
2. Add all walls of that cell to a "frontier" set.
3. While the frontier is non-empty:
   a. Pick a random wall from the frontier.
   b. If exactly one of its two cells is visited, remove the wall,
      mark the new cell visited, and add its unvisited walls to frontier.

Yields (r1,c1,r2,c2) each time a wall is removed.
"""

import random
from src.maze.grid import Grid


def prim(grid: Grid, seed: int | None = None):
    """
    Generate a perfect maze using randomized Prim.

    Args:
        grid: an empty Grid.
        seed: random seed.

    Yields:
        (r1, c1, r2, c2) each time a wall is removed.
    """
    rng = random.Random(seed)

    rows, cols = grid.rows, grid.cols
    visited = [[False] * cols for _ in range(rows)]

    start_r = rng.randrange(rows)
    start_c = rng.randrange(cols)
    visited[start_r][start_c] = True

    # frontier: list of (r1,c1, r2,c2) candidate walls
    frontier = []

    def add_walls(r: int, c: int) -> None:
        for nr, nc in grid.all_neighbors(r, c):
            if not visited[nr][nc]:
                frontier.append((r, c, nr, nc))

    add_walls(start_r, start_c)

    while frontier:
        idx = rng.randrange(len(frontier))
        frontier[idx], frontier[-1] = frontier[-1], frontier[idx]
        r1, c1, r2, c2 = frontier.pop()

        if visited[r1][c1] and not visited[r2][c2]:
            grid.remove_wall(r1, c1, r2, c2)
            visited[r2][c2] = True
            add_walls(r2, c2)
            yield r1, c1, r2, c2


def generate_prim(rows: int, cols: int, seed: int | None = None):
    """Convenience: build a complete maze and return (grid, steps)."""
    grid = Grid(rows, cols)
    steps = list(prim(grid, seed=seed))
    return grid, steps
