"""
Physical constants and the Milky Way's rotation-curve model.

Sources
-------
GRAVITY Collaboration, Abuter, R. et al. (2022). "Mass distribution in the
    Galactic Center based on interferometric astrometry of multiple stellar
    orbits." A&A, 657, L12.                                  -> M_SGR_A
GRAVITY Collaboration (2019). "A geometric distance measurement to the
    Galactic center black hole with 0.3% uncertainty." A&A, 625, L10.
                                                               -> R_SUN_KPC
Reid, M. J. & Honma, M. (2014). "Microarcsecond Radio Astrometry."
    Annual Review of Astronomy and Astrophysics, 52, 339-372. -> V_FLAT_KMS
Vallee, J. P. (2017). "A Different Pitch Angle for the Spiral Arms Traced
    by Different Astrophysical Tracers as Seen in the Milky Way Galaxy."
    ApJ, 835, 128.                                            -> PITCH_DEG
"""

import numpy as np

# ---- fundamental constants ----------------------------------------------
G = 6.674e-11            # m^3 kg^-1 s^-2
M_SUN = 1.989e30          # kg
KPC_KM = 3.0857e16        # km per kpc
YR_S = 3.1557e7           # seconds per year

# ---- Galactic-center / rotation-curve parameters -------------------------
M_SGR_A = 4.297e6 * M_SUN   # Sgr A* mass, kg
R_SUN_KPC = 8.178            # Sun's galactocentric radius, kpc
V_FLAT_KMS = 220.0            # flat rotation-curve speed, km/s (r >= R_CORE_KPC)
R_CORE_KPC = 3.0              # approx bulge/disk transition radius, kpc

# ---- spiral structure ------------------------------------------------------
GALAXY_R_KPC = 15.0    # visible disk radius used for the plot
PITCH_DEG = 12.0        # logarithmic-spiral pitch angle
B_SPIRAL = 1.0 / np.tan(np.radians(PITCH_DEG))


def v_circ_kms(r_kpc):
    """Simplified Milky Way rotation curve: solid-body rise across the
    bulge, flat beyond R_CORE_KPC. Captures the real qualitative shape
    (the actual curve is set by the disk + bulge + dark-matter halo, not
    fit here in detail) without a full mass model.
    """
    r_kpc = np.asarray(r_kpc, dtype=float)
    return np.where(r_kpc < R_CORE_KPC, V_FLAT_KMS * r_kpc / R_CORE_KPC, V_FLAT_KMS)


def omega_rad_per_myr(r_kpc):
    """Angular speed at galactocentric radius r_kpc, in rad/Myr, derived
    from the rotation curve above (omega = v_circ / r).
    """
    r_kpc = np.asarray(r_kpc, dtype=float)
    v_kms = v_circ_kms(r_kpc)
    v_kpc_per_myr = v_kms * (YR_S * 1e6) / KPC_KM
    return np.divide(v_kpc_per_myr, r_kpc, out=np.zeros_like(r_kpc), where=r_kpc > 0)


def sun_galactic_year_myr():
    """The Sun's orbital period around the Galactic center, in Myr."""
    omega = omega_rad_per_myr(R_SUN_KPC)
    return 2 * np.pi / omega


if __name__ == "__main__":
    period = sun_galactic_year_myr()
    enclosed = (V_FLAT_KMS * 1000) ** 2 * (R_SUN_KPC * KPC_KM * 1000) / G
    print(f"Sun's galactic year:  {period:.1f} Myr  (observationally: ~220-230 Myr)")
    print(f"Mass enclosed within the solar radius (order of magnitude): "
          f"{enclosed / M_SUN:.2e} Msun")
    print(f"Sgr A* itself: {M_SGR_A / M_SUN:.2e} Msun "
          f"-- almost all the enclosed mass is disk, bulge and dark-matter halo.")
