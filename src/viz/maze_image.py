"""
Fast maze-to-image conversion using a pixel grid.

Representation: a (2M+1) x (2N+1) x 3 uint8 array.
  - Odd row i, odd col j  → cell ((i-1)//2, (j-1)//2)
  - Even row/col          → wall or corner pixel

This allows O(1) wall removal (flip 1 pixel) and O(1) imshow render.

Color palette (RGB):
  WALL        = (0,   0,   0)    black
  OPEN        = (255, 255, 255)  white
  UNVISITED   = (200, 200, 200)  light gray (generation only)
  EXPLORED    = (174, 214, 241)  light blue
  PATH        = (249, 231, 159)  light yellow
  CURRENT     = (240, 165,   0)  orange
  START       = ( 39, 174,  96)  green
  GOAL        = (231,  76,  60)  red
"""

import numpy as np
from src.maze.grid import Grid, N_BIT, S_BIT, E_BIT, W_BIT

# ------------------------------------------------------------------
# Colors
# ------------------------------------------------------------------
WALL      = np.array([0,   0,   0],   dtype=np.uint8)
OPEN      = np.array([255, 255, 255], dtype=np.uint8)
UNVISITED = np.array([200, 200, 200], dtype=np.uint8)
EXPLORED  = np.array([174, 214, 241], dtype=np.uint8)
PATH_COL  = np.array([249, 231, 159], dtype=np.uint8)
CURRENT   = np.array([240, 165,   0], dtype=np.uint8)
START_COL = np.array([ 39, 174,  96], dtype=np.uint8)
GOAL_COL  = np.array([231,  76,  60], dtype=np.uint8)


def _cell_px(r: int, c: int):
    """Pixel coords of the center of cell (r,c) in the image."""
    return 1 + 2 * r, 1 + 2 * c


def _wall_px(r1: int, c1: int, r2: int, c2: int):
    """Pixel coords of the wall between two adjacent cells."""
    return (r1 + r2 + 1), (c1 + c2 + 1)


def empty_image(rows: int, cols: int, cell_color=None) -> np.ndarray:
    """
    Create a blank maze image (all walls closed, cells optionally colored).
    Shape: (2*rows+1, 2*cols+1, 3) uint8.
    """
    h = 2 * rows + 1
    w = 2 * cols + 1
    img = np.zeros((h, w, 3), dtype=np.uint8)
    # Fill cell pixels
    c = cell_color if cell_color is not None else OPEN
    img[1::2, 1::2] = c
    return img


def grid_to_image(grid: Grid, cell_color=None) -> np.ndarray:
    """
    Build a full image from a Grid, opening wall pixels for passages.
    """
    rows, cols = grid.rows, grid.cols
    img = empty_image(rows, cols, cell_color)
    for r in range(rows):
        for c in range(cols):
            for bit, (dr, dc) in [
                (N_BIT, (-1, 0)), (S_BIT, (1, 0)),
                (E_BIT, (0, 1)),  (W_BIT, (0, -1)),
            ]:
                if grid.passage[r, c] & (1 << bit):
                    wr, wc = _wall_px(r, c, r + dr, c + dc)
                    img[wr, wc] = OPEN
    return img


class MazeImageBuilder:
    """
    Incrementally build a maze image as walls are removed.
    Much faster than recomputing from scratch each frame.
    """

    def __init__(self, rows: int, cols: int, unvisited: bool = False):
        self.rows = rows
        self.cols = cols
        cell_c = UNVISITED if unvisited else OPEN
        self.img = empty_image(rows, cols, cell_c)

    def open_wall(self, r1: int, c1: int, r2: int, c2: int) -> None:
        """Remove wall between (r1,c1) and (r2,c2)."""
        wr, wc = _wall_px(r1, c1, r2, c2)
        self.img[wr, wc] = OPEN
        # Also mark both cells as visited (white)
        pr1, pc1 = _cell_px(r1, c1)
        pr2, pc2 = _cell_px(r2, c2)
        self.img[pr1, pc1] = OPEN
        self.img[pr2, pc2] = OPEN

    def highlight(self, r: int, c: int, color: np.ndarray) -> None:
        pr, pc = _cell_px(r, c)
        self.img[pr, pc] = color

    def get_frame(self, highlight_cells=None) -> np.ndarray:
        """
        Return a copy of the image with optional temporary highlights.
        highlight_cells: list of (r, c, color_array)
        """
        if not highlight_cells:
            return self.img.copy()
        frame = self.img.copy()
        for r, c, col in highlight_cells:
            pr, pc = _cell_px(r, c)
            frame[pr, pc] = col
        return frame
