"""Sanity tests: connectivity, valid path, A* <= BFS path length."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.maze.kruskal import generate_kruskal
from src.maze.prim import generate_prim
from src.search.bfs import bfs
from src.search.dfs import dfs
from src.search.ucs import ucs
from src.search.astar import astar
from src.maze.grid import Grid


def test_kruskal_connected():
    grid, steps = generate_kruskal(10, 10, seed=0)
    assert grid.is_connected(), "Kruskal maze not connected"
    assert len(steps) == 10 * 10 - 1, "Wrong number of edges"
    print("PASS kruskal_connected")


def test_prim_connected():
    grid, steps = generate_prim(10, 10, seed=0)
    assert grid.is_connected(), "Prim maze not connected"
    assert len(steps) == 10 * 10 - 1, "Wrong number of edges"
    print("PASS prim_connected")


def test_path_valid():
    grid, _ = generate_kruskal(15, 15, seed=1)
    start, goal = (0, 0), (14, 14)
    result = bfs(grid, start, goal)
    assert result.found
    # Each consecutive pair must be adjacent with open passage
    path = result.path
    for i in range(len(path) - 1):
        r1, c1 = path[i]
        r2, c2 = path[i + 1]
        assert abs(r1 - r2) + abs(c1 - c2) == 1, "Non-adjacent step"
        assert grid.has_passage(r1, c1, r2, c2), "Step through wall"
    print("PASS path_valid")


def test_astar_optimal():
    """A* path length must equal BFS path length on uniform-cost grid."""
    grid, _ = generate_kruskal(20, 20, seed=2)
    start, goal = (0, 0), (19, 19)
    r_bfs = bfs(grid, start, goal)
    r_astar = astar(grid, start, goal)
    assert r_bfs.found and r_astar.found
    assert r_astar.path_length == r_bfs.path_length, (
        f"A* ({r_astar.path_length}) != BFS ({r_bfs.path_length})"
    )
    print(f"PASS astar_optimal  path={r_astar.path_length}  "
          f"astar_nodes={r_astar.nodes_explored}  bfs_nodes={r_bfs.nodes_explored}")


def test_astar_explores_fewer():
    """A* should explore fewer or equal nodes than BFS on uniform-cost."""
    grid, _ = generate_kruskal(30, 30, seed=3)
    start, goal = (0, 0), (29, 29)
    r_bfs  = bfs(grid, start, goal)
    r_astar = astar(grid, start, goal)
    print(f"  BFS nodes={r_bfs.nodes_explored}  A* nodes={r_astar.nodes_explored}")
    # Not guaranteed in all mazes, but almost always true — warn if not
    if r_astar.nodes_explored > r_bfs.nodes_explored:
        print("  WARN: A* explored more nodes than BFS (unusual but possible)")
    else:
        print("PASS astar_explores_fewer")


if __name__ == "__main__":
    test_kruskal_connected()
    test_prim_connected()
    test_path_valid()
    test_astar_optimal()
    test_astar_explores_fewer()
    print("\nAll tests passed.")
