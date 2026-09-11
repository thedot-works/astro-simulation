"""
Run both simulations back to back.

    python main.py            # two interactive windows, one after the other
    python main.py --save     # writes solar_system.gif and milky_way.gif
"""

import argparse

import matplotlib.pyplot as plt

import solar_system
import galaxy
from constants import sun_galactic_year_myr, M_SGR_A, M_SUN

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true",
                         help="save both animations as .gif instead of opening windows")
    args = parser.parse_args()

    print("=" * 70)
    print("SOLAR SYSTEM -- Kepler's Third Law check")
    print("=" * 70)
    table = solar_system.kepler_validation_table()
    print(table[["planet", "a_AU", "T_days_observed", "T_days_kepler", "pct_error"]]
          .to_string(index=False))

    print()
    print("=" * 70)
    print("THE MILKY WAY -- structural summary")
    print("=" * 70)
    r, theta0, rgb = galaxy.build_galaxy()
    print(f"{len(r):,} stars across the bulge and four spiral arms")
    print(f"Sun's derived galactic year: {sun_galactic_year_myr():.1f} Myr "
          f"(observationally: ~220-230 Myr)")
    print(f"Sgr A* mass: {M_SGR_A / M_SUN:.3e} Msun "
          f"-- a small fraction of the mass enclosed within the solar orbit")
    print()

    fig1, anim1 = solar_system.make_animation()
    fig2, anim2 = galaxy.make_animation()

    if args.save:
        import matplotlib.animation as animation
        anim1.save("solar_system.gif", writer=animation.PillowWriter(fps=20))
        print("Saved solar_system.gif")
        anim2.save("milky_way.gif", writer=animation.PillowWriter(fps=18))
        print("Saved milky_way.gif")
    else:
        plt.show()
