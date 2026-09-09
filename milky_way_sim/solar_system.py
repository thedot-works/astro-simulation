"""
The Solar System -- eight planets on Keplerian orbits.

Orbital elements are from the NASA Planetary Fact Sheets
(Williams, D. R., NASA Goddard, nssdc.gsfc.nasa.gov/planetary/factsheet/).
Orbits are drawn circular (real eccentricities are all under 0.09 except
Mercury's 0.206, so the simplification is mild for seven of the eight
planets). Orbit radii are shown on a sqrt(a) scale purely so Mercury and
Neptune fit in one frame -- Neptune's true orbit is ~78x wider than
Mercury's.

Run directly:
    python solar_system.py            # opens an interactive window
    python solar_system.py --save     # writes solar_system.gif instead
"""

import argparse

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle

PLANETS = pd.DataFrame([
    # name       a_AU    e       T_days_observed   color       rel_radius
    ("Mercury",  0.387,  0.206,  87.97,   "#b7b2ab", 0.38),
    ("Venus",    0.723,  0.007,  224.70,  "#e8d3a0", 0.95),
    ("Earth",    1.000,  0.017,  365.25,  "#4f8ff0", 1.00),
    ("Mars",     1.524,  0.093,  686.98,  "#c1440e", 0.53),
    ("Jupiter",  5.204,  0.049,  4332.59, "#d8ae78", 11.2),
    ("Saturn",   9.583,  0.057,  10759.2, "#e3c078", 9.45),
    ("Uranus",   19.22,  0.046,  30688.5, "#9fe0e0", 4.01),
    ("Neptune",  30.05,  0.010,  60195.0, "#5b7fe0", 3.88),
], columns=["planet", "a_AU", "e", "T_days_observed", "color", "rel_radius"])


def kepler_validation_table():
    """Kepler's Third Law (Sun-dominated system, planet mass negligible):
        T[yr] = a[AU]^(3/2)
    Returns the planets table with predicted period and % error against
    the observed value, as a sanity check on the physics.
    """
    df = PLANETS.copy()
    df["T_days_kepler"] = (df["a_AU"] ** 1.5) * 365.25
    df["pct_error"] = 100 * (df["T_days_kepler"] - df["T_days_observed"]) / df["T_days_observed"]
    return df


def build_figure():
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor('#05060a')
    ax.set_facecolor('#05060a')
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("The Solar System -- orbits to sqrt(a) scale",
                  color='#eef1fb', fontsize=13, pad=12)

    r_display = np.sqrt(PLANETS["a_AU"].values)
    r_display = r_display / r_display.max() * 1.02

    for r in r_display:
        ax.add_patch(Circle((0, 0), r, fill=False, ec='#2a3350', lw=0.8, zorder=1))

    ax.scatter([0], [0], s=1400, c='#ffb15e', alpha=0.18, zorder=2)
    ax.scatter([0], [0], s=260, c='#fff3cf', zorder=3)
    ax.text(0, -0.09, "Sun", color='#fff3cf', ha='center', fontsize=9, zorder=3)

    n = len(PLANETS)
    planet_dots = ax.scatter(
        r_display, np.zeros(n),
        s=np.clip(PLANETS["rel_radius"].values * 9, 18, 130),
        c=PLANETS["color"].values, zorder=4,
    )
    labels = [ax.text(0, 0, name, color='#c9cfe3', fontsize=8, zorder=5)
              for name in PLANETS["planet"]]
    time_text = ax.set_xlabel("", color='#6b7391', fontsize=9)

    return fig, ax, r_display, planet_dots, labels


def make_animation(days_per_frame=6.0, frames=180, interval=40):
    fig, ax, r_display, planet_dots, labels = build_figure()
    n = len(PLANETS)
    theta0 = np.linspace(0, 2 * np.pi, n, endpoint=False) + 0.4
    omega = 2 * np.pi / PLANETS["T_days_observed"].values  # rad / day

    def update(frame):
        t = frame * days_per_frame
        theta = theta0 + omega * t
        x, y = r_display * np.cos(theta), r_display * np.sin(theta)
        planet_dots.set_offsets(np.column_stack([x, y]))
        for lbl, xi, yi in zip(labels, x, y):
            lbl.set_position((xi + 0.03, yi + 0.03))
        ax.set_xlabel(f"t = {t:,.0f} days ({t / 365.25:.2f} yr)",
                       color='#6b7391', fontsize=9)
        return [planet_dots, *labels]

    anim = animation.FuncAnimation(fig, update, frames=frames, interval=interval, blit=False)
    return fig, anim


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true",
                         help="save to solar_system.gif instead of opening a window")
    parser.add_argument("--frames", type=int, default=180)
    args = parser.parse_args()

    table = kepler_validation_table()
    pd.set_option("display.float_format", lambda v: f"{v:,.3f}")
    print(table[["planet", "a_AU", "T_days_observed", "T_days_kepler", "pct_error"]]
          .to_string(index=False))
    print("\nKepler's Third Law reproduces every observed period to well under 1%.\n")

    fig, anim = make_animation(frames=args.frames)

    if args.save:
        anim.save("solar_system.gif", writer=animation.PillowWriter(fps=20))
        print("Saved solar_system.gif")
    else:
        plt.show()
