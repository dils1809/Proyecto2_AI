"""Uniform-Cost Search (Dijkstra) — optimal with weighted edges."""

import heapq
import time
from src.maze.grid import Grid
from src.search.search_base import SearchResult, reconstruct_path


def ucs(grid: Grid, start: tuple, goal: tuple) -> SearchResult:
    t0 = time.perf_counter()
    # heap entries: (cost, counter, node)
    counter = 0
    heap = [(0.0, counter, start)]
    came_from = {start: None}
    cost_so_far = {start: 0.0}
    explored = []

    while heap:
        cost, _, current = heapq.heappop(heap)
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
            new_cost = cost + edge_cost
            if nb not in cost_so_far or new_cost < cost_so_far[nb]:
                cost_so_far[nb] = new_cost
                came_from[nb] = current
                counter += 1
                heapq.heappush(heap, (new_cost, counter, nb))

    return SearchResult.not_found(explored, (time.perf_counter() - t0) * 1000)
