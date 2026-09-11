"""
Act IV, correctness-pass visual: how gold got from neutron star mergers to
Earth's crust.

This is the plain, unstyled validation pass (build plan Phase 3) -- it
exists to confirm physics.earth_delivery's timeline is legible and
correctly sequenced before any Manim cinematic treatment. The timeline
spans nine orders of magnitude in time (9+ billion years of enrichment down
to a 200 Myr bombardment window), so it is drawn as two linked panels: a
compressed deep-time strip (enrichment era through solar system formation)
and a linear zoom on Earth's first ~300 Myr plus a present-day marker.

Run directly:

    python -m render.earth_timeline
"""

import textwrap

import matplotlib.pyplot as plt

from physics.earth_delivery import timeline, STAGE_COLORS, STAGE_LABELS

GOLD_COLOR = "#ffd35c"


def _labeled_point(ax, x, color, label, detail=None, level=1, wrap=18):
    """Plot one event marker with a stem leading to a label stacked at a
    given vertical 'level' (levels alternate/increase to avoid overlap),
    and an optional detail line below the axis.
    """
    y_label = 0.24 * level
    ax.plot([x, x], [0, y_label - 0.03], color=color, lw=0.9, alpha=0.6, zorder=2)
    ax.scatter([x], [0], s=85, color=color, edgecolor="#05060a", linewidth=1.1, zorder=3)
    wrapped = "\n".join(textwrap.wrap(label, wrap))
    ax.text(x, y_label, wrapped, color=color, fontsize=8.2, ha="center", va="bottom",
             fontweight="bold", zorder=4)
    if detail:
        y_detail = -0.24 * level
        ax.plot([x, x], [0, y_detail + 0.03], color=color, lw=0.9, alpha=0.4, zorder=2)
        wrapped_d = "\n".join(textwrap.wrap(detail, wrap + 4))
        ax.text(x, y_detail, wrapped_d, color="#8891ab", fontsize=6.6, ha="center", va="top", zorder=4)


def build_figure():
    events = timeline()
    fig, (ax_deep, ax_zoom) = plt.subplots(
        1, 2, figsize=(15, 7.5), gridspec_kw={"width_ratios": [1, 1.3]})
    for ax in (ax_deep, ax_zoom):
        ax.set_facecolor("#05060a")
    fig.patch.set_facecolor("#05060a")
    fig.suptitle("How gold got from neutron star mergers to Earth's crust",
                  color="#eef1fb", fontsize=14, y=0.985)

    # --- left panel: deep time, enrichment era -> solar system formation ---
    deep_events = [e for e in events if e["t_myr"] < 0]
    ax_deep.set_title("Deep time (billions of years)", color="#c9cfe3", fontsize=11, pad=45)
    ax_deep.set_xlim(-9500, 300)
    ax_deep.set_ylim(-1.3, 1.3)
    ax_deep.axhline(0, color="#2a3350", lw=1.5, zorder=1)
    ax_deep.set_yticks([])
    ax_deep.set_xlabel("Million years before solar system formation", color="#8891ab", fontsize=9)
    ax_deep.tick_params(colors="#8891ab")
    for spine in ax_deep.spines.values():
        spine.set_visible(False)

    for i, e in enumerate(deep_events):
        c = STAGE_COLORS[e["stage"]]
        level = 1 + i  # stack increasingly higher so labels never collide
        _labeled_point(ax_deep, e["t_myr"], c, e["label"], level=level, wrap=20)

    # arrow showing the span of ongoing enrichment
    ax_deep.annotate("", xy=(-80, -0.62), xytext=(-9300, -0.62),
                       arrowprops=dict(arrowstyle="->", color="#5ec9d8", lw=1.3))
    ax_deep.text(-4700, -0.74, "~9.1 Gyr of neutron star mergers enriching the galaxy",
                  color="#5ec9d8", fontsize=8.5, ha="center")

    # --- right panel: linear zoom, t=0 to ~300 Myr, plus present-day break ---
    zoom_events = [e for e in events if 0 <= e["t_myr"] <= 300]
    ax_zoom.set_title("Earth's early history (t = 0 at solar system formation)",
                        color="#c9cfe3", fontsize=11, pad=45)
    ax_zoom.set_xlim(-15, 340)
    ax_zoom.set_ylim(-1.3, 1.3)
    ax_zoom.axhline(0, color="#2a3350", lw=1.5, zorder=1)
    ax_zoom.set_yticks([])
    ax_zoom.set_xlabel("Million years after solar system formation", color="#8891ab", fontsize=9)
    ax_zoom.tick_params(colors="#8891ab")
    for spine in ax_zoom.spines.values():
        spine.set_visible(False)

    # alternate label stack level so adjacent close-together points don't collide
    zoom_levels = [1, 2, 3, 1]
    for i, e in enumerate(zoom_events):
        c = STAGE_COLORS[e["stage"]]
        level = zoom_levels[i % len(zoom_levels)]
        _labeled_point(ax_zoom, e["t_myr"], c, e["label"], detail=e["detail"], level=level, wrap=15)

    # present-day callout, off to the side (it's ~4.3 Gyr away, drawn as a break)
    ax_zoom.annotate("", xy=(330, 0.02), xytext=(280, 0.02),
                       arrowprops=dict(arrowstyle="-|>", color=GOLD_COLOR, lw=1.3))
    ax_zoom.text(305, 0.10, "...4.3 Gyr of\ngeology later...\npresent day:\nmined, refined, worn",
                  color=GOLD_COLOR, fontsize=7.5, ha="center", va="bottom", fontweight="bold")

    # shared legend
    handles = [plt.Line2D([0], [0], marker="o", color="none", markerfacecolor=STAGE_COLORS[s],
                            markersize=9, label=STAGE_LABELS[s])
               for s in ["enrichment", "formation", "differentiation", "context", "late_veneer", "present"]]
    fig.legend(handles=handles, loc="lower center", ncol=3, facecolor="#0d1220",
                edgecolor="#1c2438", labelcolor="#c9cfe3", fontsize=8.5,
                bbox_to_anchor=(0.5, 0.0))

    fig.tight_layout(rect=[0, 0.12, 1, 0.92])
    return fig, (ax_deep, ax_zoom)


if __name__ == "__main__":
    fig, axes = build_figure()
    fig.savefig("data/earth_timeline.png", dpi=150, facecolor=fig.get_facecolor())
    print("Saved data/earth_timeline.png")
