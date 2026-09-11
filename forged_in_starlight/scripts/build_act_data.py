"""
Precomputes every number the Manim cinematic scenes need into a single
data/act_data.json, so the rendering code (render/cinematic/*.py) never
re-implements physics -- it only reads numbers that physics/*.py already
computed and validated.

Run from the forged_in_starlight/ directory:
    python scripts/build_act_data.py
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from physics.rprocess import build_path, GOLD, SEED, MAGIC_N
from physics.origins import elements, CATEGORY_COLORS, CATEGORY_LABELS
from physics.earth_delivery import timeline as earth_timeline, STAGE_COLORS, STAGE_LABELS
from physics.merger import (measure_chirp_mass, orbital_separation_track,
                              measure_frequency_ridge, chirp_mass_from_point,
                              PUBLISHED_CHIRP_MASS_MSUN, T_MERGER, DATA_DIR)

OUT_PATH = Path(__file__).resolve().parent.parent / "data" / "act_data.json"


def _whitened_strain_snippet(det="H1", half_window_s=0.3, max_points=1200):
    """Real whitened strain amplitude vs. time-relative-to-merger, for the
    waveform figure. Downsampled only for file size / render speed -- the
    underlying series is the same real, whitened GWOSC data physics.merger
    already validated the chirp against.
    """
    from gwpy.timeseries import TimeSeries
    path = DATA_DIR / f"gw170817_{det}_whitened.hdf5"
    ts = TimeSeries.read(str(path))
    seg = ts.crop(T_MERGER - half_window_s, T_MERGER)
    t_rel = seg.times.value - T_MERGER
    y = seg.value
    step = max(1, len(t_rel) // max_points)
    return t_rel[::step].tolist(), (y[::step] / np.max(np.abs(y))).tolist()


def main():
    path = build_path()
    els = elements()
    earth = earth_timeline()

    mc = measure_chirp_mass()
    t, a = orbital_separation_track()

    # downsample the orbital track to ~300 points for a smooth but light
    # animation; np.unique also drops any duplicate indices from rounding
    idx = np.unique(np.geomspace(1, len(t), 300).astype(int) - 1)
    t_ds = t[idx].tolist()
    a_ds = a[idx].tolist()

    # full (unfiltered) frequency ridge for the chirp-mass figure, plus the
    # analytic post-Newtonian fit curve evaluated at the measured chirp mass
    ridge_t, ridge_f, ridge_p = measure_frequency_ridge(det="H1")
    mc_kg = mc["chirp_mass_msun_measured"] * 1.989e30
    from physics.merger import G, C
    fit_t = np.linspace(0.02, ridge_t.max(), 200)
    fit_f = (1.0 / np.pi) * (5.0 / 256.0) ** (3.0 / 8.0) * (G * mc_kg / C ** 3) ** (-5.0 / 8.0) * fit_t ** (-3.0 / 8.0)

    waveform_t, waveform_y = _whitened_strain_snippet(det="H1")

    out = {
        "rprocess_path": path,
        "gold": GOLD, "seed": SEED, "magic_n": list(MAGIC_N),
        "elements": els,
        "category_colors": CATEGORY_COLORS, "category_labels": CATEGORY_LABELS,
        "earth_timeline": earth,
        "stage_colors": STAGE_COLORS, "stage_labels": STAGE_LABELS,
        "chirp_mass_measured": mc["chirp_mass_msun_measured"],
        "chirp_mass_measured_std": mc["chirp_mass_msun_std"],
        "chirp_mass_published": PUBLISHED_CHIRP_MASS_MSUN,
        "orbital_t_before_merger": t_ds,
        "orbital_separation_km": a_ds,
        "ridge_t_before_merger": ridge_t.tolist(),
        "ridge_f_gw": ridge_f.tolist(),
        "ridge_power": ridge_p.tolist(),
        "fit_t_before_merger": fit_t.tolist(),
        "fit_f_gw": fit_f.tolist(),
        "waveform_t_before_merger": waveform_t,
        "waveform_strain_normalized": waveform_y,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(out, f)
    print(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
