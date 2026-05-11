"""
Problema 3 — Comparación de algoritmos de búsqueda.

Ejecuta K=25 escenarios en grids 45×55, corre BFS/DFS/UCS/A* en cada
uno y produce:
  - results/data/raw_metrics.csv
  - results/data/ranking_summary.csv
  - results/plots/bar_nodes.png
  - results/plots/bar_time.png
  - results/plots/bar_path.png
  - results/plots/ranking_summary.png
  - results/plots/scenario_table.png
  - results/gifs/p3_sample_<algo>.gif  (para el escenario 1, los 4 algos)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.benchmark.runner import run_benchmark
from src.viz.plots import (
    plot_metric_bars, plot_ranking_summary, plot_scenario_table
)
from src.maze.kruskal import generate_kruskal
from src.search.bfs import bfs
from src.search.dfs import dfs
from src.search.ucs import ucs
from src.search.astar import astar
from src.viz.animate_search import animate_search
import random

DATA_DIR  = os.path.join(os.path.dirname(__file__), "..", "results", "data")
PLOT_DIR  = os.path.join(os.path.dirname(__file__), "..", "results", "plots")
GIF_DIR   = os.path.join(os.path.dirname(__file__), "..", "results", "gifs")


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(PLOT_DIR, exist_ok=True)
    os.makedirs(GIF_DIR,  exist_ok=True)

    # ------------------------------------------------------------------ #
    # Benchmark K=25
    # ------------------------------------------------------------------ #
    print("=== Benchmark K=25 escenarios ===")
    raw_df, ranking_df = run_benchmark(k=25, weighted=True)

    raw_df.to_csv(os.path.join(DATA_DIR, "raw_metrics.csv"), index=False)
    ranking_df.to_csv(os.path.join(DATA_DIR, "ranking_summary.csv"), index=False)
    print("\nRanking final:")
    print(ranking_df.to_string(index=False))

    # ------------------------------------------------------------------ #
    # Plots comparativos
    # ------------------------------------------------------------------ #
    print("\n=== Generando plots ===")
    plot_metric_bars(
        raw_df, "nodes_explored", "Nodos explorados (promedio)",
        "Nodos explorados por algoritmo",
        os.path.join(PLOT_DIR, "bar_nodes.png"),
    )
    plot_metric_bars(
        raw_df, "time_ms", "Tiempo (ms)",
        "Tiempo de ejecución por algoritmo",
        os.path.join(PLOT_DIR, "bar_time.png"),
    )
    # path_length: solo cuando found=True
    found_df = raw_df[raw_df["path_length"] > 0].copy()
    plot_metric_bars(
        found_df, "path_length", "Longitud de ruta",
        "Longitud de ruta óptima por algoritmo",
        os.path.join(PLOT_DIR, "bar_path.png"),
    )
    plot_ranking_summary(ranking_df, os.path.join(PLOT_DIR, "ranking_summary.png"))
    plot_scenario_table(raw_df, os.path.join(PLOT_DIR, "scenario_table.png"))

    # ------------------------------------------------------------------ #
    # GIFs de muestra: escenario 1 con los 4 algoritmos
    # ------------------------------------------------------------------ #
    print("\n=== GIFs de muestra (escenario 1) ===")
    ROWS, COLS = 45, 55
    sample_grid, _ = generate_kruskal(ROWS, COLS, seed=0)
    rng = random.Random(0)
    start = (2, 2)
    goal  = (ROWS - 3, COLS - 3)

    algo_fns = {"BFS": bfs, "DFS": dfs, "UCS": ucs, "Astar": astar}
    for name, fn in algo_fns.items():
        result = fn(sample_grid, start, goal)
        animate_search(
            sample_grid, result, start, goal,
            out_path=os.path.join(GIF_DIR, f"p3_sample_{name.lower()}.gif"),
            title=f"{name}  45×55",
            n_frames=120, fps=15,
            figsize=(8, 6), dpi=80,
        )

    print("\n=== Problema 3 completo ===")
    print(f"  Datos:  {os.path.abspath(DATA_DIR)}")
    print(f"  Plots:  {os.path.abspath(PLOT_DIR)}")
    print(f"  GIFs:   {os.path.abspath(GIF_DIR)}")


if __name__ == "__main__":
    main()
