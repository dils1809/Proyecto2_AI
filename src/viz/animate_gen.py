"""
Animate maze generation and save to GIF.
Uses pixel-image rendering (imshow) — much faster than per-wall plot calls.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import io

from src.maze.grid import Grid
from src.viz.maze_image import MazeImageBuilder, CURRENT


def animate_generation(grid: Grid, steps: list, out_path: str,
                       title: str = "Maze Generation",
                       n_frames: int = 120,
                       fps: int = 20,
                       figsize: tuple = (6, 5),
                       dpi: int = 80) -> None:
    """
    Save an animated GIF of maze construction.

    Args:
        grid: the finished Grid (passages already set — used only for size).
        steps: list of (r1,c1,r2,c2) from the generator.
        out_path: output GIF file path.
        n_frames: approx number of frames to render.
        fps: frames per second.
    """
    rows, cols = grid.rows, grid.cols
    total = len(steps)
    skip = max(1, total // n_frames)
    selected = set(range(0, total, skip))
    selected.add(total - 1)

    builder = MazeImageBuilder(rows, cols, unvisited=True)

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.axis("off")
    fig.suptitle(title, fontsize=10)
    im_obj = ax.imshow(builder.img, interpolation="nearest", aspect="equal")
    fig.tight_layout(rect=[0, 0, 1, 0.95])

    frames_pil = []

    for i, (r1, c1, r2, c2) in enumerate(steps):
        builder.open_wall(r1, c1, r2, c2)

        if i in selected:
            frame = builder.get_frame([(r1, c1, CURRENT), (r2, c2, CURRENT)])
            im_obj.set_data(frame)
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight",
                        facecolor="white")
            buf.seek(0)
            frames_pil.append(Image.open(buf).copy().convert("P"))
            buf.close()

    # Final clean frame
    im_obj.set_data(builder.img)
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
    print(f"  Saved: {out_path}  ({len(frames_pil)} frames)")
