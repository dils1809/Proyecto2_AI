"""
Grid representation for mazes.

Each cell stores its open passages as a bitmask:
  bit 0 = North, bit 1 = South, bit 2 = East, bit 3 = West
All bits start at 0 (all walls closed). Removing a wall sets the bit.
"""

import numpy as np

N_BIT = 0  # North
S_BIT = 1  # South
E_BIT = 2  # East
W_BIT = 3  # West

OPPOSITE = {N_BIT: S_BIT, S_BIT: N_BIT, E_BIT: W_BIT, W_BIT: E_BIT}
DR = {N_BIT: -1, S_BIT: 1, E_BIT: 0, W_BIT: 0}
DC = {N_BIT: 0, S_BIT: 0, E_BIT: 1, W_BIT: -1}


class Grid:
    """M-row × N-col maze grid."""

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        # passage[r,c] = bitmask of open directions
        self.passage = np.zeros((rows, cols), dtype=np.uint8)
        # optional cost layer (default 1 everywhere)
        self.cost = np.ones((rows, cols), dtype=np.float32)

    # ------------------------------------------------------------------
    # Wall operations
    # ------------------------------------------------------------------

    def _valid(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def remove_wall(self, r1: int, c1: int, r2: int, c2: int) -> None:
        """Open the passage between adjacent cells (r1,c1) and (r2,c2)."""
        dr, dc = r2 - r1, c2 - c1
        if dr == -1:
            direction = N_BIT
        elif dr == 1:
            direction = S_BIT
        elif dc == 1:
            direction = E_BIT
        else:
            direction = W_BIT
        self.passage[r1, c1] |= (1 << direction)
        self.passage[r2, c2] |= (1 << OPPOSITE[direction])

    def has_passage(self, r1: int, c1: int, r2: int, c2: int) -> bool:
        dr, dc = r2 - r1, c2 - c1
        if dr == -1:
            direction = N_BIT
        elif dr == 1:
            direction = S_BIT
        elif dc == 1:
            direction = E_BIT
        else:
            direction = W_BIT
        return bool(self.passage[r1, c1] & (1 << direction))

    # ------------------------------------------------------------------
    # Neighbor queries
    # ------------------------------------------------------------------

    def all_neighbors(self, r: int, c: int):
        """All 4 grid neighbors (regardless of walls)."""
        for bit in (N_BIT, S_BIT, E_BIT, W_BIT):
            nr, nc = r + DR[bit], c + DC[bit]
            if self._valid(nr, nc):
                yield nr, nc

    def passage_neighbors(self, r: int, c: int):
        """Neighbors reachable through open passages (for search)."""
        for bit in (N_BIT, S_BIT, E_BIT, W_BIT):
            if self.passage[r, c] & (1 << bit):
                nr, nc = r + DR[bit], c + DC[bit]
                yield nr, nc

    def passage_cost(self, r: int, c: int):
        """Yields (nr, nc, cost) for each open passage from (r,c)."""
        for bit in (N_BIT, S_BIT, E_BIT, W_BIT):
            if self.passage[r, c] & (1 << bit):
                nr, nc = r + DR[bit], c + DC[bit]
                yield nr, nc, float(self.cost[nr, nc])

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def all_cells(self):
        for r in range(self.rows):
            for c in range(self.cols):
                yield r, c

    def all_edges(self):
        """All potential edges (pairs of adjacent cells), each listed once."""
        for r in range(self.rows):
            for c in range(self.cols):
                if r + 1 < self.rows:
                    yield (r, c, r + 1, c)
                if c + 1 < self.cols:
                    yield (r, c, r, c + 1)

    def is_connected(self) -> bool:
        """BFS connectivity check."""
        visited = set()
        stack = [(0, 0)]
        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))
            for nr, nc in self.passage_neighbors(r, c):
                stack.append((nr, nc))
        return len(visited) == self.rows * self.cols


class UnionFind:
    """Weighted Union-Find with path compression."""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True
