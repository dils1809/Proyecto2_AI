"""
Benchmark runner for Problem 3.

For each of K scenarios:
  - Generate a random maze (45×55) with Kruskal or Prim alternating.
  - Sample start A and goal B with manhattan(A,B) >= 10.
  - Run BFS, DFS, UCS, A* and record metrics.
  - Assign per-scenario rank (1=best) by: found desc, path_length asc, time_ms asc.
  - Return a DataFrame with all raw rows + a ranking summary DataFrame.
"""

import random
import pandas as pd

from src.maze.kruskal import generate_kruskal
from src.maze.prim import generate_prim
from src.search.bfs import bfs
from src.search.dfs import dfs
from src.search.ucs import ucs
from src.search.astar import astar
from src.maze.grid import Grid
import numpy as np

ALGORITHMS = {
    "BFS": bfs,
    "DFS": dfs,
    "UCS": ucs,
    "A*":  astar,
}

ROWS, COLS = 45, 55
K = 25
MIN_MANHATTAN = 10


def _sample_endpoints(rows: int, cols: int, min_dist: int, rng: random.Random):
    while True:
        r1, c1 = rng.randrange(rows), rng.randrange(cols)
        r2, c2 = rng.randrange(rows), rng.randrange(cols)
        if abs(r1 - r2) + abs(c1 - c2) >= min_dist:
            return (r1, c1), (r2, c2)


def _add_terrain_weights(grid: Grid, rng: random.Random, n_patches: int = 6):
    """Add Voronoi-like weighted patches to the grid cost layer."""
    rows, cols = grid.rows, grid.cols
    centers = [(rng.randrange(rows), rng.randrange(cols)) for _ in range(n_patches)]
    weights = [rng.choice([1, 2, 3, 5]) for _ in range(n_patches)]

    for r in range(rows):
        for c in range(cols):
            dists = [abs(r - cr) + abs(c - cc) for cr, cc in centers]
            nearest = int(np.argmin(dists))
            grid.cost[r, c] = weights[nearest]


def run_benchmark(k: int = K, weighted: bool = True) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Run K scenarios and return (raw_df, ranking_df).

    raw_df columns:
      scenario, seed, algorithm, start, goal,
      nodes_explored, time_ms, path_length, found, rank

    ranking_df columns:
      algorithm, avg_rank, best_count (rank==1 count)
    """
    rows_data = []

    for scenario in range(k):
        seed = scenario
        rng = random.Random(seed)

        # Alternate generators
        if scenario % 2 == 0:
            grid, _ = generate_kruskal(ROWS, COLS, seed=seed)
        else:
            grid, _ = generate_prim(ROWS, COLS, seed=seed)

        # Add weighted terrain in half the scenarios
        if weighted and scenario % 2 == 0:
            _add_terrain_weights(grid, rng)

        start, goal = _sample_endpoints(ROWS, COLS, MIN_MANHATTAN, rng)

        scenario_results = []
        for algo_name, algo_fn in ALGORITHMS.items():
            result = algo_fn(grid, start, goal)
            scenario_results.append({
                "scenario": scenario + 1,
                "seed": seed,
                "algorithm": algo_name,
                "start": str(start),
                "goal": str(goal),
                "nodes_explored": result.nodes_explored,
                "time_ms": round(result.time_ms, 4),
                "path_length": result.path_length if result.found else float("inf"),
                "found": result.found,
                "rank": 0,
            })

        # Rank within scenario
        scenario_results.sort(key=lambda x: (
            not x["found"],               # found first
            x["path_length"],             # shorter path
            x["time_ms"],                 # faster
        ))
        for rank, row in enumerate(scenario_results, start=1):
            row["rank"] = rank

        rows_data.extend(scenario_results)
        print(f"  Escenario {scenario + 1:2d}/{k}  start={start} goal={goal}  "
              + "  ".join(
                  f"{r['algorithm']}:{r['rank']}" for r in scenario_results
              ))

    raw_df = pd.DataFrame(rows_data)
    raw_df["path_length"] = raw_df["path_length"].replace(float("inf"), -1)

    # Ranking summary
    ranking_rows = []
    for algo in ALGORITHMS:
        sub = raw_df[raw_df["algorithm"] == algo]
        ranking_rows.append({
            "algorithm": algo,
            "avg_rank": round(sub["rank"].mean(), 3),
            "best_count": int((sub["rank"] == 1).sum()),
            "avg_nodes": round(sub["nodes_explored"].mean(), 1),
            "avg_time_ms": round(sub["time_ms"].mean(), 4),
            "avg_path_length": round(sub[sub["path_length"] > 0]["path_length"].mean(), 1),
        })
    ranking_df = pd.DataFrame(ranking_rows).sort_values("avg_rank")

    return raw_df, ranking_df
