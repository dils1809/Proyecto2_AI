"""
Exporta imágenes PNG estáticas para el reporte LaTeX.
Genera capturas de momentos clave de generación y búsqueda.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from src.maze.kruskal import generate_kruskal
from src.maze.prim import generate_prim
from src.search.astar import astar
from src.search.bfs import bfs
from src.search.dfs import dfs
from src.search.ucs import ucs
from src.viz.maze_image import (
    MazeImageBuilder, grid_to_image, _cell_px,
    EXPLORED, PATH_COL, START_COL, GOAL_COL, CURRENT, UNVISITED, OPEN
)
from src.maze.grid import Grid

FIGS = os.path.join(os.path.dirname(__file__), "..", "report", "figs")
os.makedirs(FIGS, exist_ok=True)

DPI = 120


def save_png(fig, name):
    path = os.path.join(FIGS, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {name}")


# ---------------------------------------------------------------
# Helper: draw image in a figure
# ---------------------------------------------------------------
def fig_from_img(img, title="", figsize=(7, 5)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(img, interpolation="nearest", aspect="equal")
    ax.axis("off")
    if title:
        fig.suptitle(title, fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95] if title else [0,0,1,1])
    return fig


# ---------------------------------------------------------------
# P1 — Generación: estado intermedio + final para Kruskal y Prim
# ---------------------------------------------------------------
print("=== P1: Generación ===")
ROWS_G, COLS_G = 30, 40

for algo_name, gen_fn in [("kruskal", generate_kruskal), ("prim", generate_prim)]:
    grid, steps = gen_fn(ROWS_G, COLS_G, seed=42)
    total = len(steps)

    # Estado ~30% de construcción
    builder30 = MazeImageBuilder(ROWS_G, COLS_G, unvisited=True)
    cut = total // 3
    for r1, c1, r2, c2 in steps[:cut]:
        builder30.open_wall(r1, c1, r2, c2)
    r1, c1, r2, c2 = steps[cut - 1]
    img30 = builder30.get_frame([(r1, c1, CURRENT), (r2, c2, CURRENT)])
    fig = fig_from_img(img30, f"{'Kruskal' if algo_name=='kruskal' else 'Prim'} — construcción (~30%)", (7, 5))
    save_png(fig, f"{algo_name}_mid.png")

    # Estado final
    builder_full = MazeImageBuilder(ROWS_G, COLS_G, unvisited=True)
    for r1, c1, r2, c2 in steps:
        builder_full.open_wall(r1, c1, r2, c2)
    fig = fig_from_img(builder_full.img, f"{'Kruskal' if algo_name=='kruskal' else 'Prim'} — laberinto final ({ROWS_G}×{COLS_G})", (7, 5))
    save_png(fig, f"{algo_name}_final.png")


# ---------------------------------------------------------------
# P2 — A* y BFS resolviendo 60×80
# ---------------------------------------------------------------
print("=== P2: Búsqueda 60×80 ===")
ROWS_S, COLS_S = 60, 80
grid60, _ = generate_kruskal(ROWS_S, COLS_S, seed=7)
start60, goal60 = (0, 0), (ROWS_S - 1, COLS_S - 1)

base = grid_to_image(grid60)

def overlay_search(base_img, result, start, goal, mid_frac=0.5):
    explored = result.explored
    path = result.path if result.found else []
    cut = int(len(explored) * mid_frac)

    # Mid exploration
    mid = base_img.copy()
    for r, c in explored[:cut]:
        pr, pc = _cell_px(r, c)
        mid[pr, pc] = EXPLORED
    pr, pc = _cell_px(*explored[cut-1])
    mid[pr, pc] = CURRENT
    pr, pc = _cell_px(*start); mid[pr, pc] = START_COL
    pr, pc = _cell_px(*goal);  mid[pr, pc] = GOAL_COL

    # Final with path
    final = base_img.copy()
    for r, c in explored:
        pr, pc = _cell_px(r, c)
        final[pr, pc] = EXPLORED
    for r, c in path:
        pr, pc = _cell_px(r, c)
        final[pr, pc] = PATH_COL
    pr, pc = _cell_px(*start); final[pr, pc] = START_COL
    pr, pc = _cell_px(*goal);  final[pr, pc] = GOAL_COL
    return mid, final

for algo_name, algo_fn in [("astar", astar), ("bfs", bfs)]:
    result = algo_fn(grid60, start60, goal60)
    label = "A*" if algo_name == "astar" else "BFS"
    mid_img, final_img = overlay_search(base, result, start60, goal60)

    fig = fig_from_img(mid_img, f"{label} — exploración en progreso (60×80)", (9, 7))
    save_png(fig, f"p2_{algo_name}_mid.png")

    fig = fig_from_img(final_img,
        f"{label} — solución encontrada  |  longitud={result.path_length}  nodos={result.nodes_explored}", (9, 7))
    save_png(fig, f"p2_{algo_name}_final.png")


# ---------------------------------------------------------------
# P3 — Los 4 algoritmos resolviendo el mismo laberinto 45×55
# ---------------------------------------------------------------
print("=== P3: Comparación 4 algoritmos ===")
ROWS_P, COLS_P = 45, 55
grid45, _ = generate_kruskal(ROWS_P, COLS_P, seed=0)
start45, goal45 = (2, 2), (ROWS_P - 3, COLS_P - 3)
base45 = grid_to_image(grid45)

algo_map = {"BFS": bfs, "DFS": dfs, "UCS": ucs, "A*": astar}
results45 = {name: fn(grid45, start45, goal45) for name, fn in algo_map.items()}

# Panel 2×2 con los 4 finales
fig, axes = plt.subplots(2, 2, figsize=(12, 9))
fig.suptitle("Comparación de algoritmos — laberinto 45×55", fontsize=13)
for ax, (name, res) in zip(axes.flat, results45.items()):
    img = base45.copy()
    for r, c in res.explored:
        pr, pc = _cell_px(r, c)
        img[pr, pc] = EXPLORED
    for r, c in res.path:
        pr, pc = _cell_px(r, c)
        img[pr, pc] = PATH_COL
    pr, pc = _cell_px(*start45); img[pr, pc] = START_COL
    pr, pc = _cell_px(*goal45);  img[pr, pc] = GOAL_COL
    ax.imshow(img, interpolation="nearest", aspect="equal")
    ax.axis("off")
    ax.set_title(
        f"{name}  |  nodos={res.nodes_explored}  longitud={res.path_length}",
        fontsize=10
    )
fig.tight_layout()
save_png(fig, "p3_comparison_panel.png")

# Individual por algo
for name, res in results45.items():
    img = base45.copy()
    for r, c in res.explored:
        pr, pc = _cell_px(r, c)
        img[pr, pc] = EXPLORED
    for r, c in res.path:
        pr, pc = _cell_px(r, c)
        img[pr, pc] = PATH_COL
    pr, pc = _cell_px(*start45); img[pr, pc] = START_COL
    pr, pc = _cell_px(*goal45);  img[pr, pc] = GOAL_COL
    fig = fig_from_img(img,
        f"{name}  |  nodos explorados={res.nodes_explored}  longitud={res.path_length}  tiempo={res.time_ms:.2f}ms",
        (8, 6))
    save_png(fig, f"p3_{name.lower().replace('*','star')}_final.png")

print(f"\nTodas las figuras guardadas en: {os.path.abspath(FIGS)}")
print("Sube la carpeta report/figs/ completa a Overleaf.")
