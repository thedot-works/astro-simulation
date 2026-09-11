"""
Act III, correctness-pass visual: an animated nuclide chart (N vs Z)
tracing the r-process waiting-point path from an iron seed up to gold.

This is the plain, unstyled validation pass (build plan Phase 3) -- it
exists to confirm physics.rprocess's path is correct and legible before
any Manim cinematic treatment. Run directly:

    python -m render.nuclide_chart
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

from physics.rprocess import build_path, stability_valley_z, MAGIC_N, GOLD, SEED

GOLD_COLOR = "#ffd35c"      # the one hue reserved for gold, consistent with the
                             # rest of the project's visual identity
CAPTURE_COLOR = "#5ec9d8"    # neutron capture -- cool cyan
DECAY_COLOR = "#ff6a3d"       # beta decay -- warm orange (matches the kilonova's
                              # "red" lanthanide-rich ejecta color)


def build_figure():
    fig, ax = plt.subplots(figsize=(8, 7))
    fig.patch.set_facecolor("#05060a")
    ax.set_facecolor("#05060a")

    n_max, z_max = 165, 90
    ax.set_xlim(20, n_max)
    ax.set_ylim(15, z_max)
    ax.set_xlabel("Neutron number N", color="#c9cfe3")
    ax.set_ylabel("Proton number Z", color="#c9cfe3")
    ax.set_title("The r-process: an iron seed climbing to gold",
                  color="#eef1fb", fontsize=13, pad=12)
    ax.tick_params(colors="#8891ab")
    for spine in ax.spines.values():
        spine.set_color("#2a3350")

    # valley of stability
    n_grid = np.linspace(20, n_max, 300)
    a_grid = n_grid + stability_valley_z(n_grid + n_grid)  # rough iterative guess
    # solve self-consistently: Z_stable depends on A = N + Z, so iterate a couple times
    z_stable = stability_valley_z(n_grid * 2)
    for _ in range(4):
        z_stable = stability_valley_z(n_grid + z_stable)
    ax.plot(n_grid, z_stable, color="#4a5170", lw=1.5, ls="--", label="Valley of stability")

    # magic-number shell closures (the waiting points)
    for n_magic in MAGIC_N:
        ax.axvline(n_magic, color="#3a4160", lw=1, alpha=0.6)
        ax.text(n_magic, z_max - 3, f"N={n_magic}", color="#6b7391", fontsize=8,
                 ha="center", va="top")

    # seed and gold markers
    ax.scatter([SEED["N"]], [SEED["Z"]], s=70, facecolor="none",
               edgecolor="#c9cfe3", linewidths=1.5, zorder=5)
    ax.text(SEED["N"] + 2, SEED["Z"] - 3, "Fe-56 seed", color="#c9cfe3", fontsize=9)

    gold_marker = Rectangle((GOLD["N"] - 1.5, GOLD["Z"] - 1.5), 3, 3,
                              facecolor="none", edgecolor=GOLD_COLOR, linewidth=2, zorder=5)
    ax.add_patch(gold_marker)
    ax.text(GOLD["N"] + 3, GOLD["Z"], "Au-197\n(gold)", color=GOLD_COLOR, fontsize=9.5,
             fontweight="bold", va="center")

    path_line, = ax.plot([], [], color=CAPTURE_COLOR, lw=1.5, alpha=0.85, zorder=4)
    path_dot = ax.scatter([], [], s=26, c="#eef1fb", zorder=6)
    time_text = ax.text(0.02, 0.03, "", transform=ax.transAxes, color="#8891ab", fontsize=9)

    handles = [
        plt.Line2D([0], [0], color=CAPTURE_COLOR, lw=2, label="Rapid neutron capture"),
        plt.Line2D([0], [0], color=DECAY_COLOR, lw=2, label="Beta decay (waiting point)"),
    ]
    leg = ax.legend(handles=handles, loc="lower right", facecolor="#0d1220",
                     edgecolor="#1c2438", labelcolor="#c9cfe3", fontsize=9)

    return fig, ax, path_line, path_dot, time_text


def make_animation(steps_per_frame=1):
    path = build_path()
    ns = [p["N"] for p in path]
    zs = [p["Z"] for p in path]
    stages = [p["stage"] for p in path]

    fig, ax, path_line, path_dot, time_text = build_figure()

    # precompute per-segment colors so the trail can show capture vs decay
    segment_colors = []
    for i in range(1, len(path)):
        segment_colors.append(DECAY_COLOR if "decay" in stages[i] else CAPTURE_COLOR)

    lines = [ax.plot([], [], lw=1.8, alpha=0.9, zorder=4)[0] for _ in segment_colors]

    def update(frame):
        idx = min(frame * steps_per_frame, len(path) - 1)
        for i in range(idx):
            lines[i].set_data([ns[i], ns[i + 1]], [zs[i], zs[i + 1]])
            lines[i].set_color(segment_colors[i])
        path_dot.set_offsets([[ns[idx], zs[idx]]])
        reached_gold = (zs[idx], ns[idx]) == (GOLD["Z"], GOLD["N"])
        path_dot.set_color(GOLD_COLOR if reached_gold else "#eef1fb")
        path_dot.set_sizes([140 if reached_gold else 26])
        time_text.set_text(f"step {idx+1}/{len(path)}   t ~ {path[idx]['t']:.2f} s (illustrative)"
                             + ("   -- GOLD" if reached_gold else ""))
        return [*lines, path_dot, time_text]

    n_frames = len(path) + 8  # hold a beat at the end on gold
    anim = animation.FuncAnimation(fig, update, frames=n_frames, interval=60, blit=False)
    return fig, anim, path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true", help="save to nuclide_chart.gif")
    args = parser.parse_args()

    fig, anim, path = make_animation()
    if args.save:
        anim.save("data/nuclide_chart.gif", writer=animation.PillowWriter(fps=16))
        print("Saved data/nuclide_chart.gif")
    else:
        plt.show()
