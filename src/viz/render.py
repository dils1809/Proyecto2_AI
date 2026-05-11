"""
Base maze rendering with matplotlib.

Color scheme:
  wall   = black
  cell   = white
  start  = green
  goal   = red
  explored = light blue
  path   = yellow
  current = orange
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from src.maze.grid import Grid, N_BIT, S_BIT, E_BIT, W_BIT, DR, DC

WALL_W = 0.08   # wall stroke relative to cell size


def draw_maze(ax: plt.Axes, grid: Grid,
              explored=None, path=None,
              start=None, goal=None,
              current=None,
              cell_size: float = 1.0) -> None:
    """
    Draw the maze onto ax.

    Args:
        ax: matplotlib Axes (must have been set up externally).
        grid: the Grid to draw.
        explored: iterable of (r,c) cells to shade as explored.
        path: iterable of (r,c) cells to shade as the solution path.
        start/goal: (r,c) tuples.
        current: (r,c) cell currently being processed.
        cell_size: pixel-like unit (axes coordinates).
    """
    rows, cols = grid.rows, grid.cols
    cs = cell_size

    ax.set_xlim(0, cols * cs)
    ax.set_ylim(0, rows * cs)
    ax.set_aspect("equal")
    ax.axis("off")

    # Background
    ax.set_facecolor("white")

    # Explored cells
    if explored:
        for r, c in explored:
            rect = patches.Rectangle(
                (c * cs, (rows - 1 - r) * cs), cs, cs,
                linewidth=0, facecolor="#AED6F1"
            )
            ax.add_patch(rect)

    # Path cells
    if path:
        for r, c in path:
            rect = patches.Rectangle(
                (c * cs, (rows - 1 - r) * cs), cs, cs,
                linewidth=0, facecolor="#F9E79F"
            )
            ax.add_patch(rect)

    # Current cell
    if current:
        r, c = current
        rect = patches.Rectangle(
            (c * cs, (rows - 1 - r) * cs), cs, cs,
            linewidth=0, facecolor="#F0A500"
        )
        ax.add_patch(rect)

    # Start / Goal
    for cell, color in [(start, "#27AE60"), (goal, "#E74C3C")]:
        if cell:
            r, c = cell
            rect = patches.Rectangle(
                (c * cs, (rows - 1 - r) * cs), cs, cs,
                linewidth=0, facecolor=color
            )
            ax.add_patch(rect)

    # Walls
    lw = WALL_W * cs * 6
    for r in range(rows):
        for c in range(cols):
            x0 = c * cs
            y0 = (rows - 1 - r) * cs
            passage = grid.passage[r, c]
            # Draw missing walls
            if not (passage & (1 << N_BIT)):  # North wall (top of cell)
                ax.plot([x0, x0 + cs], [y0 + cs, y0 + cs], "k-", lw=lw)
            if not (passage & (1 << S_BIT)):  # South wall (bottom)
                ax.plot([x0, x0 + cs], [y0, y0], "k-", lw=lw)
            if not (passage & (1 << E_BIT)):  # East wall (right)
                ax.plot([x0 + cs, x0 + cs], [y0, y0 + cs], "k-", lw=lw)
            if not (passage & (1 << W_BIT)):  # West wall (left)
                ax.plot([x0, x0], [y0, y0 + cs], "k-", lw=lw)

    # Outer border
    border = patches.Rectangle(
        (0, 0), cols * cs, rows * cs,
        linewidth=lw, edgecolor="black", facecolor="none"
    )
    ax.add_patch(border)
