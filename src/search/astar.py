"""A* Search with Manhattan-distance heuristic."""

import heapq
import time
from src.maze.grid import Grid
from src.search.search_base import SearchResult, reconstruct_path


def manhattan(a: tuple, b: tuple) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid: Grid, start: tuple, goal: tuple) -> SearchResult:
    t0 = time.perf_counter()
    counter = 0
    h = manhattan(start, goal)
    heap = [(h, counter, start)]
    came_from = {start: None}
    g = {start: 0.0}
    explored = []

    while heap:
        _, _, current = heapq.heappop(heap)
        if current in explored:
            continue
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
        for nr, nc, edge_cost in grid.passage_cost(r, c):
            nb = (nr, nc)
            new_g = g[current] + edge_cost
            if nb not in g or new_g < g[nb]:
                g[nb] = new_g
                came_from[nb] = current
                f = new_g + manhattan(nb, goal)
                counter += 1
                heapq.heappush(heap, (f, counter, nb))

    return SearchResult.not_found(explored, (time.perf_counter() - t0) * 1000)
