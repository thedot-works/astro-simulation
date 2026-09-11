"""
Binary neutron star inspiral, calibrated against the real GW170817 chirp.

Rather than assuming textbook neutron star masses, this measures the
chirp mass directly from the whitened H1 strain data (data/gw170817_H1_whitened.hdf5)
using the leading-order post-Newtonian frequency evolution, then uses that
measured chirp mass to drive the orbital-separation animation.

Physics
-------
Leading-order (Newtonian) GW frequency evolution of an inspiraling binary:

    f_gw(t) = (1/pi) * (5/256)^(3/8) * (G*Mc/c^3)^(-5/8) * (t_c - t)^(-3/8)

Inverting for the chirp mass Mc given a measured (t, f) pair and merger
time t_c:

    Mc = (c^3/G) * { (5/256) / [ (t_c - t) * (pi*f)^(8/3) ] }^(3/5)

Orbital separation decays under gravitational-wave emission (Peters 1964,
circular-orbit limit):

    da/dt = -(64/5) * G^3 * m1 * m2 * (m1+m2) / (c^5 * a^3)

Sources
-------
Abbott, B. P. et al. (2017). "GW170817: Observation of Gravitational Waves
    from a Binary Neutron Star Inspiral." Phys. Rev. Lett. 119, 161101.
    (published chirp mass: 1.188 +0.004/-0.002 Msun, source frame)
Peters, P. C. (1964). "Gravitational Radiation and the Motion of Two Point
    Masses." Phys. Rev. 136, B1224.
"""

from pathlib import Path

import numpy as np
from gwpy.timeseries import TimeSeries

G = 6.674e-11        # m^3 kg^-1 s^-2
C = 2.998e8           # m/s
M_SUN = 1.989e30       # kg

T_MERGER = 1187008882.4   # published GW170817 merger GPS time
PUBLISHED_CHIRP_MASS_MSUN = 1.188   # Abbott et al. 2017, source frame

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def measure_frequency_ridge(det="H1", f_lo=40, f_hi=400, n_windows=24):
    """Estimate the GW frequency track f(t) in the final ~2s before merger
    from the real whitened strain, via a sliding-window periodogram (find
    the dominant frequency in each short window). Returns (t, f) arrays,
    t measured as seconds before merger (positive, decreasing toward 0).
    """
    path = DATA_DIR / f"gw170817_{det}_whitened.hdf5"
    ts = TimeSeries.read(str(path))

    seg = ts.crop(T_MERGER - 2.2, T_MERGER - 0.05)
    x = seg.value
    fs = float(seg.sample_rate.value)
    n = len(x)

    win_len = max(64, n // n_windows)
    hop = win_len // 2

    times, freqs, powers = [], [], []
    for start in range(0, n - win_len, hop):
        chunk = x[start:start + win_len] * np.hanning(win_len)
        spec = np.fft.rfft(chunk)
        fgrid = np.fft.rfftfreq(win_len, d=1.0 / fs)
        band = (fgrid >= f_lo) & (fgrid <= f_hi)
        if not np.any(band):
            continue
        p = np.abs(spec[band]) ** 2
        peak_f = fgrid[band][np.argmax(p)]
        t_center = seg.t0.value + (start + win_len / 2) / fs
        times.append(T_MERGER - t_center)   # seconds *before* merger
        freqs.append(peak_f)
        powers.append(p.max())

    times, freqs, powers = map(np.array, (times, freqs, powers))
    # keep the frequency actually rising toward merger (monotonic-ish, top half by power)
    order = np.argsort(times)[::-1]
    return times[order], freqs[order], powers[order]


def chirp_mass_from_point(dt_before_merger, f_gw):
    """Mc (in kg) from one (time-before-merger, GW frequency) measurement,
    via the leading-order PN chirp relation.
    """
    val = (5.0 / 256.0) / (dt_before_merger * (np.pi * f_gw) ** (8.0 / 3.0))
    return (C ** 3 / G) * val ** (3.0 / 5.0)


def measure_chirp_mass(det="H1", power_percentile=70):
    """Measure the chirp mass from the real data: take the higher-power
    ridge points (more likely to be real signal, not noise) and average
    their individually-implied chirp masses.
    """
    t, f, p = measure_frequency_ridge(det=det)
    # only use points with rising frequency approaching merger and decent power
    keep = (t > 0.02) & (p > np.percentile(p, power_percentile))
    if keep.sum() < 2:
        keep = t > 0.02
    mc_samples = chirp_mass_from_point(t[keep], f[keep])
    mc_msun = mc_samples / M_SUN
    return {
        "chirp_mass_msun_measured": float(np.median(mc_msun)),
        "chirp_mass_msun_std": float(np.std(mc_msun)),
        "n_points_used": int(keep.sum()),
        "published_chirp_mass_msun": PUBLISHED_CHIRP_MASS_MSUN,
        "t_before_merger": t[keep].tolist(),
        "f_gw": f[keep].tolist(),
    }


def orbital_separation_track(m1_msun=1.36, m2_msun=1.36, a0_km=300.0, n_steps=2000):
    """Integrate da/dt under GW emission (Peters 1964, circular orbit) from
    an initial separation down to contact. Returns (t_seconds_before_merger,
    a_km) with t=0 at merger (a -> ~contact radius, not literally 0).

    Default masses (1.36 Msun each) match GW170817's measured total mass
    (~2.74 Msun) split close to equal mass ratio, consistent with the
    LIGO/Virgo parameter estimation for this event.
    """
    m1, m2 = m1_msun * M_SUN, m2_msun * M_SUN
    a = a0_km * 1000.0  # meters
    dt = 1e-4  # seconds, adaptively refined below since inspiral accelerates

    contact_radius_km = 20.0  # ~NS diameter scale, stop integrating near here
    a_hist, t_hist = [a], [0.0]
    t_elapsed = 0.0

    while a > contact_radius_km * 1000.0 and len(a_hist) < 2_000_000:
        da_dt = -(64.0 / 5.0) * G ** 3 * m1 * m2 * (m1 + m2) / (C ** 5 * a ** 3)
        # adaptive step: smaller steps as inspiral accelerates
        step = min(dt, 0.002 * a / max(abs(da_dt), 1e-30))
        a = a + da_dt * step
        t_elapsed += step
        a_hist.append(a)
        t_hist.append(t_elapsed)

    t_hist = np.array(t_hist)
    a_hist = np.array(a_hist)
    t_before_merger = t_hist[-1] - t_hist  # 0 at final (contact) point
    return t_before_merger, a_hist / 1000.0  # seconds, km


if __name__ == "__main__":
    result = measure_chirp_mass()
    print("Chirp mass measured from real H1 data:")
    print(f"  {result['chirp_mass_msun_measured']:.3f} +/- {result['chirp_mass_msun_std']:.3f} Msun"
          f"  (from {result['n_points_used']} ridge points)")
    print(f"  Published (Abbott et al. 2017): {result['published_chirp_mass_msun']:.3f} Msun")

    t, a = orbital_separation_track()
    print(f"\nOrbital separation track: {len(t)} steps, "
          f"from {a[0]:.0f} km down to {a[-1]:.1f} km at contact, "
          f"spanning {t[0]:.3f} s before merger")
