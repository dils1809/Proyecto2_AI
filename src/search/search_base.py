"""Common types shared by all search algorithms."""

from dataclasses import dataclass, field


@dataclass
class SearchResult:
    path: list          # list of (r,c) from start to goal, empty if not found
    explored: list      # list of (r,c) in order of exploration
    nodes_explored: int
    path_length: int    # number of steps (edges) in path
    time_ms: float
    found: bool

    @classmethod
    def not_found(cls, explored: list, time_ms: float) -> "SearchResult":
        return cls(
            path=[],
            explored=explored,
            nodes_explored=len(explored),
            path_length=0,
            time_ms=time_ms,
            found=False,
        )


def reconstruct_path(came_from: dict, start: tuple, goal: tuple) -> list:
    path = []
    node = goal
    while node != start:
        path.append(node)
        node = came_from[node]
    path.append(start)
    path.reverse()
    return path
