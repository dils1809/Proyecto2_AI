"""
Problema 2 — Resolver un laberinto 60×80 con A*.

Genera el laberinto con Kruskal, resuelve con A* desde (0,0) hasta
(59,79) (0-indexed equivalente al (1,1)→(60,80) del enunciado), anima
la búsqueda y muestra estadísticas finales.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.maze.kruskal import generate_kruskal
from src.search.astar import astar
from src.search.bfs import bfs
from src.viz.animate_search import animate_search

ROWS, COLS = 60, 80
SEED = 7
START = (0, 0)       # (1,1) 1-indexed
GOAL  = (ROWS-1, COLS-1)   # (60,80) 1-indexed
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "results", "gifs")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print(f"Generando laberinto {ROWS}×{COLS} con Kruskal (seed={SEED})…")
    grid, _ = generate_kruskal(ROWS, COLS, seed=SEED)

    print("Resolviendo con A*…")
    result = astar(grid, START, GOAL)

    if result.found:
        print(f"  Encontrado: longitud={result.path_length}  "
              f"nodos explorados={result.nodes_explored}  "
              f"tiempo={result.time_ms:.2f} ms")
    else:
        print("  No se encontró camino.")

    print("Generando animación A*…")
    animate_search(
        grid, result, START, GOAL,
        out_path=os.path.join(OUT_DIR, "p2_astar.gif"),
        title=f"A*  {ROWS}×{COLS}",
        n_frames=150, fps=18,
        figsize=(9, 7), dpi=80,
    )

    # Bonus: también resolver con BFS para comparar en el reporte
    print("Resolviendo con BFS (comparación)…")
    result_bfs = bfs(grid, START, GOAL)
    print(f"  BFS: longitud={result_bfs.path_length}  "
          f"nodos explorados={result_bfs.nodes_explored}  "
          f"tiempo={result_bfs.time_ms:.2f} ms")

    animate_search(
        grid, result_bfs, START, GOAL,
        out_path=os.path.join(OUT_DIR, "p2_bfs.gif"),
        title=f"BFS  {ROWS}×{COLS}",
        n_frames=150, fps=18,
        figsize=(9, 7), dpi=80,
    )

    print("\nProblema 2 completo.")
    print(f"  GIFs guardados en: {os.path.abspath(OUT_DIR)}")


if __name__ == "__main__":
    main()
