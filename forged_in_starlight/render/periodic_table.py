"""
Act I, correctness-pass visual: the periodic table colored by astrophysical
origin (build plan Phase 3), with gold picked out.

This is the plain, unstyled validation pass -- it exists to confirm
physics.origins' classification is correct and legible before any Manim
cinematic treatment. Two outputs:

  build_figure()   a static table, every element colored by its dominant
                    origin, gold outlined and labeled
  make_animation()  the same table built up category by category (Big Bang
                    first, then cosmic rays, stellar fusion, supernovae,
                    AGB stars, and finally neutron star mergers -- roughly
                    the order in cosmic history these channels turned on),
                    ending on gold lighting up

Run directly:

    python -m render.periodic_table
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

from physics.origins import elements, CATEGORY_COLORS, CATEGORY_LABELS, GOLD_Z

GOLD_COLOR = "#ffd35c"

# rough cosmic-history ordering of when each channel first started producing
# elements -- used to sequence the build-up animation
CATEGORY_ORDER = [
    "big_bang",
    "cosmic_ray_fission",
    "stellar_fusion",
    "exploding_massive_stars",
    "exploding_white_dwarfs",
    "dying_low_mass_stars",
    "merging_neutron_stars",
    "human_made",
]

CELL_W, CELL_H = 0.92, 0.92


def _cell_xy(e):
    """Map (period, group) to plot coordinates. Lanthanide/actinide rows
    (period 8, 9) are drawn as detached rows below the main body, with a
    gap row for visual separation, matching the conventional layout.
    """
    x = e["group"]
    period = e["period"]
    if period <= 7:
        y = 8 - period  # period 1 at top
    else:
        y = 8 - 7 - 1.2 - (period - 8) * 1.0  # detached f-block rows below
    return x, y


def build_figure(highlight_categories=None):
    """highlight_categories: if given, only elements in these categories are
    colored; the rest are drawn as empty outlines. None means show all.
    """
    fig, ax = plt.subplots(figsize=(13, 7.5))
    fig.patch.set_facecolor("#05060a")
    ax.set_facecolor("#05060a")
    ax.set_xlim(0, 19)
    ax.set_ylim(-3.6, 9.4)
    ax.axis("off")
    ax.set_title("Where every element comes from",
                  color="#eef1fb", fontsize=15, pad=14)

    cells = {}
    for e in elements():
        x, y = _cell_xy(e)
        active = highlight_categories is None or e["category"] in highlight_categories
        face = e["color"] if active else "#0d1220"
        edge = GOLD_COLOR if e["is_gold"] else ("#2a3350" if active else "#1c2438")
        lw = 2.2 if e["is_gold"] else 0.8
        rect = Rectangle((x - CELL_W / 2, y - CELL_H / 2), CELL_W, CELL_H,
                          facecolor=face, edgecolor=edge, linewidth=lw, zorder=3)
        ax.add_patch(rect)
        txt_color = "#05060a" if active and e["category"] not in ("human_made",) else "#c9cfe3"
        if e["is_gold"]:
            txt_color = "#3a2c00"
        ax.text(x, y + 0.16, e["symbol"], ha="center", va="center",
                 fontsize=9.5, fontweight="bold" if e["is_gold"] else "normal",
                 color=txt_color, zorder=4)
        ax.text(x, y - 0.28, str(e["Z"]), ha="center", va="center",
                 fontsize=5.5, color=txt_color, alpha=0.8, zorder=4)
        cells[e["Z"]] = rect

    gold = next(e for e in elements() if e["is_gold"])
    gx, gy = _cell_xy(gold)
    ax.annotate("Gold -- forged in\nneutron star mergers",
                 xy=(gx, gy + CELL_H / 2), xytext=(gx, 8.8),
                 color=GOLD_COLOR, fontsize=10, fontweight="bold", ha="center",
                 arrowprops=dict(arrowstyle="->", color=GOLD_COLOR, lw=1.4))

    # legend
    handles = [plt.Rectangle((0, 0), 1, 1, facecolor=CATEGORY_COLORS[c], edgecolor="none",
                               label=CATEGORY_LABELS[c])
               for c in CATEGORY_ORDER]
    ax.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.0, -0.02),
               ncol=2, facecolor="#0d1220", edgecolor="#1c2438", labelcolor="#c9cfe3",
               fontsize=8.5, framealpha=0.95)

    return fig, ax, cells


def make_animation():
    """Build up the table category by category, in rough cosmic-history
    order, ending with the r-process (and gold) lighting up last.
    """
    fig, ax, cells = build_figure(highlight_categories=set())
    els_by_cat = {}
    for e in elements():
        els_by_cat.setdefault(e["category"], []).append(e)

    frames = []
    shown = set()
    for cat in CATEGORY_ORDER:
        shown.add(cat)
        frames.append((cat, frozenset(shown)))

    caption = ax.text(0.5, 1.045, "", transform=ax.transAxes, ha="center",
                       color="#eef1fb", fontsize=12, fontweight="bold")

    def update(frame_idx):
        cat, shown_now = frames[min(frame_idx, len(frames) - 1)]
        for e in elements():
            active = e["category"] in shown_now
            rect = cells[e["Z"]]
            rect.set_facecolor(e["color"] if active else "#0d1220")
            if e["is_gold"] and active:
                rect.set_edgecolor(GOLD_COLOR)
                rect.set_linewidth(2.4)
        caption.set_text(CATEGORY_LABELS[cat])
        return [caption, *cells.values()]

    n_frames = len(frames) + 6  # hold on the finished table
    anim = animation.FuncAnimation(fig, update, frames=n_frames, interval=900, blit=False)
    return fig, anim


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true", help="save to data/periodic_table.gif")
    parser.add_argument("--static", action="store_true", help="save static full table instead")
    args = parser.parse_args()

    if args.static:
        fig, ax, cells = build_figure()
        fig.savefig("data/periodic_table_by_origin.png", dpi=150, facecolor=fig.get_facecolor())
        print("Saved data/periodic_table_by_origin.png")
    else:
        fig, anim = make_animation()
        if args.save:
            anim.save("data/periodic_table.gif", writer=animation.PillowWriter(fps=1.2))
            print("Saved data/periodic_table.gif")
        else:
            plt.show()
