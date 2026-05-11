"""
Problema 1 — Generación de laberintos aleatorios.

Genera un laberinto con Kruskal y otro con Prim, anima ambas
construcciones y guarda los GIFs en results/gifs/.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.maze.kruskal import generate_kruskal
from src.maze.prim import generate_prim
from src.viz.animate_gen import animate_generation

ROWS, COLS = 30, 40
SEED = 42
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "results", "gifs")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print("Kruskal —")
    grid_k, steps_k = generate_kruskal(ROWS, COLS, seed=SEED)
    animate_generation(
        grid_k, steps_k,
        out_path=os.path.join(OUT_DIR, "kruskal_gen.gif"),
        title=f"Kruskal  ({ROWS}×{COLS})",
        n_frames=150, fps=20,
        figsize=(7, 5), dpi=80,
    )

    print("Prim —")
    grid_p, steps_p = generate_prim(ROWS, COLS, seed=SEED)
    animate_generation(
        grid_p, steps_p,
        out_path=os.path.join(OUT_DIR, "prim_gen.gif"),
        title=f"Prim  ({ROWS}×{COLS})",
        n_frames=150, fps=20,
        figsize=(7, 5), dpi=80,
    )

    print("\nProblema 1 completo.")
    print(f"  GIFs guardados en: {os.path.abspath(OUT_DIR)}")


if __name__ == "__main__":
    main()
