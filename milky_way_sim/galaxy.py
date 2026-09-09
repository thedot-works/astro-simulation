"""
The Milky Way -- spiral structure rotating around Sagittarius A*.

Four logarithmic spiral arms (r = r0 * exp(b*theta), pitch angle ~12 deg)
approximate the Galaxy's grand-design structure (Perseus, Sagittarius-
Carina, Scutum-Centaurus, Norma-Cygnus), plus the Sun's minor Orion Spur.
A denser, warmer-colored nuclear bulge fills the inner few kiloparsecs.

Every star's angular speed comes from the same measured rotation-curve
function (see constants.py), so the field rotates *differentially* --
inner stars complete a revolution faster than outer ones -- exactly as
the real Galaxy does, rather than spinning as a rigid disk.

Run directly:
    python galaxy.py            # opens an interactive window
    python galaxy.py --save     # writes milky_way.gif instead
"""

import argparse

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle

from constants import (
    GALAXY_R_KPC, B_SPIRAL, R_SUN_KPC, omega_rad_per_myr, sun_galactic_year_myr,
)

RNG = np.random.default_rng(20260909)

ARM_OFFSETS = {
    "Perseus Arm":          0.0,
    "Sagittarius Arm":      np.pi / 2,
    "Scutum-Centaurus Arm": np.pi,
    "Norma Arm":            3 * np.pi / 2,
}
ARM_COLORS = {
    "Perseus Arm":          (143, 214, 255),
    "Sagittarius Arm":      (199, 168, 255),
    "Scutum-Centaurus Arm": (255, 176, 160),
    "Norma Arm":            (160, 200, 190),
}


def _build_arm(offset, n=650, r0=1.0):
    theta = RNG.uniform(0, 3.4, n)
    r = r0 * np.exp(B_SPIRAL * theta * 0.3)
    r = np.clip(r, 1.5, GALAXY_R_KPC)
    theta_full = theta + offset + RNG.normal(0, 0.12, n) * (0.4 + r / GALAXY_R_KPC)
    r = r * (1 + RNG.normal(0, 0.05, n))
    return r, theta_full


def build_galaxy():
    """Returns (r_kpc, theta0, rgb) arrays for every star in the field:
    the nuclear bulge, the four spiral arms, and the Sun's Orion Spur.
    """
    arm_r, arm_theta, arm_rgb = [], [], []
    for name, offset in ARM_OFFSETS.items():
        r, th = _build_arm(offset)
        arm_r.append(r)
        arm_theta.append(th)
        arm_rgb.append(np.tile(np.array(ARM_COLORS[name]) / 255.0, (len(r), 1)))
    arm_r = np.concatenate(arm_r)
    arm_theta = np.concatenate(arm_theta)
    arm_rgb = np.concatenate(arm_rgb)

    # Orion Spur -- the Sun's minor local spur, between Sagittarius and Perseus
    spur_r, spur_theta = _build_arm(np.pi / 2 + 0.55, n=200, r0=1.0)
    spur_rgb = np.tile(np.array([255, 226, 122]) / 255.0, (len(spur_r), 1))

    # nuclear bulge
    n_bulge = 500
    bulge_r = RNG.power(1.6, n_bulge) * 3.0 + 0.2
    bulge_theta = RNG.uniform(0, 2 * np.pi, n_bulge)
    bulge_rgb = np.tile(np.array([255, 214, 168]) / 255.0, (n_bulge, 1))

    all_r = np.concatenate([bulge_r, arm_r, spur_r])
    all_theta0 = np.concatenate([bulge_theta, arm_theta, spur_theta])
    all_rgb = np.concatenate([bulge_rgb, arm_rgb, spur_rgb])
    return all_r, all_theta0, all_rgb


def build_figure(all_r, all_theta0, all_rgb):
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor('#05060a')
    ax.set_facecolor('#05060a')
    ax.set_xlim(-GALAXY_R_KPC * 1.05, GALAXY_R_KPC * 1.05)
    ax.set_ylim(-GALAXY_R_KPC * 1.05, GALAXY_R_KPC * 1.05)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("The Milky Way -- top-down view, rotating about Sagittarius A*",
                  color='#eef1fb', fontsize=13, pad=12)

    for radius, alpha in [(2.6, 0.05), (1.6, 0.10), (0.9, 0.22)]:
        ax.add_patch(Circle((0, 0), radius, color='#ff9c4d', alpha=alpha, zorder=2))
    ax.scatter([0], [0], s=40, c='black', edgecolors='#ffcf9e', linewidths=1, zorder=5)
    ax.text(0.4, -0.9, "Sagittarius A*", color='#ffd7a8', fontsize=8.5, zorder=6)

    sun_theta0 = np.pi * 0.15
    ax.add_patch(Circle((0, 0), R_SUN_KPC, fill=False, ec='#ffe27a',
                          lw=1.0, alpha=0.5, zorder=1))

    star_scatter = ax.scatter(
        all_r * np.cos(all_theta0), all_r * np.sin(all_theta0),
        s=2.2, c=all_rgb, alpha=0.85, linewidths=0, zorder=3,
    )
    sun_dot = ax.scatter(
        [R_SUN_KPC * np.cos(sun_theta0)], [R_SUN_KPC * np.sin(sun_theta0)],
        s=90, c='#fff3cf', zorder=6,
    )
    sun_label = ax.text(0, 0, "Sun", color='#fff3cf', fontsize=9, zorder=6)
    time_label = ax.text(-GALAXY_R_KPC * 1.0, GALAXY_R_KPC * 0.95, "",
                           color='#6b7391', fontsize=9)

    return fig, ax, star_scatter, sun_dot, sun_label, time_label, sun_theta0


def make_animation(myr_per_frame=1.6, frames=140, interval=45):
    all_r, all_theta0, all_rgb = build_galaxy()
    all_omega = omega_rad_per_myr(all_r)
    sun_omega = omega_rad_per_myr(R_SUN_KPC)
    sun_period_myr = sun_galactic_year_myr()

    fig, ax, star_scatter, sun_dot, sun_label, time_label, sun_theta0 = build_figure(
        all_r, all_theta0, all_rgb
    )

    def update(frame):
        t = frame * myr_per_frame
        theta = all_theta0 + all_omega * t
        star_scatter.set_offsets(np.column_stack([all_r * np.cos(theta), all_r * np.sin(theta)]))

        st = sun_theta0 + sun_omega * t
        sx, sy = R_SUN_KPC * np.cos(st), R_SUN_KPC * np.sin(st)
        sun_dot.set_offsets([[sx, sy]])
        sun_label.set_position((sx + 0.4, sy + 0.4))
        time_label.set_text(
            f"t = {t:,.0f} Myr   ({t / sun_period_myr:.2f} galactic years elapsed)"
        )
        return [star_scatter, sun_dot, sun_label, time_label]

    anim = animation.FuncAnimation(fig, update, frames=frames, interval=interval, blit=False)
    return fig, anim


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true",
                         help="save to milky_way.gif instead of opening a window")
    parser.add_argument("--frames", type=int, default=140)
    args = parser.parse_args()

    r, theta0, rgb = build_galaxy()
    print(f"{len(r):,} stars placed across the bulge and four spiral arms.")
    print(f"Sun's galactic year: {sun_galactic_year_myr():.1f} Myr "
          f"(observationally: ~220-230 Myr)")

    fig, anim = make_animation(frames=args.frames)

    if args.save:
        anim.save("milky_way.gif", writer=animation.PillowWriter(fps=18))
        print("Saved milky_way.gif")
    else:
        plt.show()
