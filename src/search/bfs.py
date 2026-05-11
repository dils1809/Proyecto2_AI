"""Breadth-First Search — optimal for uniform-cost grids."""

import time
from collections import deque
from src.maze.grid import Grid
from src.search.search_base import SearchResult, reconstruct_path


def bfs(grid: Grid, start: tuple, goal: tuple) -> SearchResult:
    t0 = time.perf_counter()
    queue = deque([start])
    came_from = {start: None}
    explored = []

    while queue:
        current = queue.popleft()
        explored.append(current)

        if current == goal:
            path = reconstruct_path(came_from, start, goal)
            return SearchResult(
                path=path,
                explored=explored,
                nodes_explored=len(explored),
                path_length=len(path) - 1,
                time_ms=(time.perf_counter() - t0) * 1000,
                found=True,
            )

        r, c = current
        for nr, nc in grid.passage_neighbors(r, c):
            nb = (nr, nc)
            if nb not in came_from:
                came_from[nb] = current
                queue.append(nb)

    return SearchResult.not_found(explored, (time.perf_counter() - t0) * 1000)
