"""
Comparative plots for Problem 3 benchmark results.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

ALGO_COLORS = {
    "BFS": "#3498DB",
    "DFS": "#E74C3C",
    "UCS": "#2ECC71",
    "A*":  "#9B59B6",
}
ALGOS = ["BFS", "DFS", "UCS", "A*"]


def plot_metric_bars(df: pd.DataFrame, metric: str, ylabel: str,
                     title: str, out_path: str) -> None:
    """Bar chart: mean ± std of `metric` per algorithm."""
    fig, ax = plt.subplots(figsize=(7, 4), dpi=100)

    means = [df[df["algorithm"] == a][metric].mean() for a in ALGOS]
    stds  = [df[df["algorithm"] == a][metric].std() for a in ALGOS]
    colors = [ALGO_COLORS[a] for a in ALGOS]

    bars = ax.bar(ALGOS, means, color=colors, alpha=0.85, yerr=stds,
                  capsize=5, edgecolor="black", linewidth=0.7)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=12)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

    for bar, mean in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() * 1.02,
                f"{mean:.1f}", ha="center", va="bottom", fontsize=9)

    fig.tight_layout()
    fig.savefig(out_path, dpi=100, bbox_inches="tight")
    plt.close(fig)
    print(f"  Plot saved: {out_path}")


def plot_ranking_summary(ranking_df: pd.DataFrame, out_path: str) -> None:
    """Horizontal bar chart of average ranking (lower = better)."""
    fig, ax = plt.subplots(figsize=(6, 3), dpi=100)

    means = ranking_df.set_index("algorithm").loc[ALGOS, "avg_rank"]
    colors = [ALGO_COLORS[a] for a in ALGOS]

    bars = ax.barh(ALGOS[::-1], means[::-1], color=colors[::-1],
                   alpha=0.85, edgecolor="black", linewidth=0.7)
    ax.set_xlabel("Ranking promedio (1 = mejor)", fontsize=11)
    ax.set_title("Ranking promedio sobre K=25 escenarios", fontsize=12)
    ax.xaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

    for bar, val in zip(bars, means[::-1]):
        ax.text(val + 0.02, bar.get_y() + bar.get_height() / 2,
                f"{val:.2f}", va="center", fontsize=9)

    fig.tight_layout()
    fig.savefig(out_path, dpi=100, bbox_inches="tight")
    plt.close(fig)
    print(f"  Plot saved: {out_path}")


def plot_scenario_table(scenario_df: pd.DataFrame, out_path: str) -> None:
    """Save a visual table (matplotlib) of per-scenario metrics."""
    algos = ALGOS
    scenarios = sorted(scenario_df["scenario"].unique())
    k = len(scenarios)

    fig, ax = plt.subplots(figsize=(10, max(4, k * 0.35 + 1)), dpi=100)
    ax.axis("off")

    col_labels = ["Escenario"] + [f"{a}\nnodos" for a in algos] + \
                 [f"{a}\nms" for a in algos] + [f"{a}\nlongitud" for a in algos] + \
                 ["Ganador"]
    rows_data = []
    for s in scenarios:
        sub = scenario_df[scenario_df["scenario"] == s]
        row = [str(s)]
        for metric in ["nodes_explored", "time_ms", "path_length"]:
            for a in algos:
                val = sub[sub["algorithm"] == a][metric].values
                row.append(f"{val[0]:.1f}" if len(val) else "-")
        winner_row = sub.loc[sub["rank"] == 1, "algorithm"]
        row.append(winner_row.values[0] if len(winner_row) else "-")
        rows_data.append(row)

    table = ax.table(
        cellText=rows_data,
        colLabels=col_labels,
        cellLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(7)
    table.scale(1, 1.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=100, bbox_inches="tight")
    plt.close(fig)
    print(f"  Table saved: {out_path}")
