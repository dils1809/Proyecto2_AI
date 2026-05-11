"""
Animate a search algorithm solving a maze and save to GIF.
Uses pixel-image rendering (imshow) — fast single imshow update per frame.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import io
import numpy as np

from src.maze.grid import Grid
from src.search.search_base import SearchResult
from src.viz.maze_image import (
    grid_to_image, _cell_px,
    EXPLORED, PATH_COL, CURRENT, START_COL, GOAL_COL
)


def animate_search(grid: Grid, result: SearchResult,
                   start: tuple, goal: tuple,
                   out_path: str,
                   title: str = "Search",
                   n_frames: int = 120,
                   fps: int = 18,
                   figsize: tuple = (8, 6),
                   dpi: int = 80) -> None:
    """Save an animated GIF of search exploration + final path."""
    rows, cols = grid.rows, grid.cols
    base_img = grid_to_image(grid)

    explored = result.explored
    path = result.path if result.found else []

    total = len(explored)
    skip = max(1, total // n_frames)
    selected = list(range(0, total, skip))
    if total - 1 not in selected:
        selected.append(total - 1)

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.axis("off")
    im_obj = ax.imshow(base_img, interpolation="nearest", aspect="equal")
    title_obj = fig.suptitle(title, fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.95])

    frames_pil = []

    def make_frame(explored_slice, show_path=False):
        frame = base_img.copy()
        for r, c in explored_slice:
            pr, pc = _cell_px(r, c)
            frame[pr, pc] = EXPLORED
        if show_path:
            for r, c in path:
                pr, pc = _cell_px(r, c)
                frame[pr, pc] = PATH_COL
        # Current cell
        if explored_slice:
            r, c = explored_slice[-1]
            pr, pc = _cell_px(r, c)
            frame[pr, pc] = CURRENT
        # Start / goal always on top
        pr, pc = _cell_px(*start)
        frame[pr, pc] = START_COL
        pr, pc = _cell_px(*goal)
        frame[pr, pc] = GOAL_COL
        return frame

    for i in selected:
        subset = explored[: i + 1]
        frame = make_frame(subset, show_path=False)
        im_obj.set_data(frame)
        title_obj.set_text(f"{title}  |  nodos explorados: {i + 1}")
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", facecolor="white")
        buf.seek(0)
        frames_pil.append(Image.open(buf).copy().convert("P"))
        buf.close()

    # Final frames with path highlighted
    final_frame = make_frame(explored, show_path=True)
    im_obj.set_data(final_frame)
    title_obj.set_text(
        f"{title}  |  longitud: {result.path_length}  |  nodos: {result.nodes_explored}"
    )
    hold_frames = max(3, fps // 2)
    for _ in range(hold_frames):
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", facecolor="white")
        buf.seek(0)
        frames_pil.append(Image.open(buf).copy().convert("P"))
        buf.close()

    plt.close(fig)

    duration = int(1000 / fps)
    frames_pil[0].save(
        out_path,
        save_all=True,
        append_images=frames_pil[1:],
        loop=0,
        duration=duration,
        optimize=True,
    )
    print(f"  Saved: {out_path}  ({len(frames_pil)} frames, "
          f"path={result.path_length}, explored={result.nodes_explored})")
