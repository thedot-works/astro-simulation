"""
The AT2017gfo kilonova -- bolometric light curve from three real ejecta
components, using an Arnett-type radioactive-decay diffusion model.

Each component's mass, velocity, and opacity are the actual best-fit
values published in Villar et al. (2017). The opacity is what encodes
composition: low opacity (blue) means light, lanthanide-poor r-process
elements; high opacity (red) means the lanthanide-rich, gold/platinum/
uranium-bearing ejecta -- lanthanides have many more electron transitions
than lighter elements, which trap optical/UV light and push the emission
redward. The famous blue-to-red color evolution of a kilonova over its
first ~10 days *is* watching the light r-process material fade while the
heavy r-process material (gold's neighborhood) takes over.

Model
-----
Arnett-style diffusion (Arnett 1982; adapted for kilonovae by Metzger
et al. 2010, and used in this specific form by Villar et al. 2017):

    L(t) = exp(-t^2/td^2) * integral_0^t [ L_in(t') * eps_th(t') *
                                             exp(t'^2/td^2) * (t'/td) ] dt'

    td = sqrt( 2 * kappa * M_ej / (beta * v_ej * c) )      [diffusion time]

Radioactive heating rate (Korobkin et al. 2012 fitting formula, the
standard r-process heating-rate approximation used across the kilonova
literature):

    L_in(t) = M_ej * eps0 * [ 0.5 - (1/pi) * arctan((t - t0) / sigma) ]^1.3

Thermalization efficiency declines as gamma-rays/leptons escape the
ejecta (Barnes et al. 2016 fitting form):

    eps_th(t) = 0.36 * [ exp(-a*t) + ln(1 + 2*b*t^d) / (2*b*t^d) ]

Sources
-------
Villar, V. A. et al. (2017). "The Combined Ultraviolet, Optical, and
    Near-infrared Light Curves of the Kilonova Associated with the Binary
    Neutron Star Merger GW170817." ApJL, 851, L21.
    (three-component fit: this is where the mass/velocity/opacity values
    for the blue, purple, and red components come from)
Korobkin, O. et al. (2012). "On the astrophysical robustness of the
    neutron star merger r-process." MNRAS, 426, 1940.
Barnes, J. et al. (2016). "Effects of r-Process Heating on Fallback
    Accretion in Compact Object Mergers." ApJ, 829, 110.
Arnett, W. D. (1982). "Type I supernovae. I - Analytic solutions for the
    early part of the light curve." ApJ, 253, 785.
"""

import numpy as np

C_CGS = 2.998e10          # cm/s
M_SUN_G = 1.989e33          # g
DAY_S = 86400.0

BETA = 13.8   # geometric constant in the Arnett diffusion-time formula

# Villar et al. (2017) three-component best fit for AT2017gfo
COMPONENTS = {
    "blue": {
        "mass_msun": 0.020,
        "v_frac_c": 0.27,
        "kappa": 0.5,       # cm^2/g
        "color": "#7ec8ff",
        "label": "Blue (lanthanide-poor)",
    },
    "purple": {
        "mass_msun": 0.047,
        "v_frac_c": 0.15,
        "kappa": 3.0,
        "color": "#b98bff",
        "label": "Purple (intermediate)",
    },
    "red": {
        "mass_msun": 0.011,
        "v_frac_c": 0.14,
        "kappa": 10.0,
        "color": "#ff6a3d",
        "label": "Red (lanthanide-rich -- gold's neighborhood)",
    },
}

# Korobkin et al. (2012) heating-rate fit constants (standard r-process values)
EPS0 = 2.0e18       # erg / g / s
SIGMA = 0.11        # s
T0 = 1.3            # s

# Barnes et al. (2016) thermalization-efficiency fit constants (typical r-process ejecta)
BARNES_A, BARNES_B, BARNES_D = 0.56, 0.17, 1.21


def diffusion_time_s(mass_msun, v_frac_c, kappa):
    m = mass_msun * M_SUN_G
    v = v_frac_c * C_CGS
    return np.sqrt(2 * kappa * m / (BETA * v * C_CGS))


def heating_rate(t_s, mass_msun):
    """Korobkin (2012) r-process radioactive heating rate, erg/s, for a
    component of the given ejecta mass.
    """
    m = mass_msun * M_SUN_G
    shape = (0.5 - (1.0 / np.pi) * np.arctan((t_s - T0) / SIGMA)) ** 1.3
    return m * EPS0 * shape


def thermalization_efficiency(t_s):
    t_days = t_s / DAY_S
    term1 = np.exp(-BARNES_A * t_days)
    x = 2 * BARNES_B * t_days ** BARNES_D
    term2 = np.log1p(x) / np.where(x > 0, x, 1.0)
    return 0.36 * (term1 + term2)


def component_luminosity(t_s, mass_msun, v_frac_c, kappa, n_integration=4000):
    """Bolometric luminosity (erg/s) of one ejecta component vs time,
    via the Arnett diffusion integral.
    """
    td = diffusion_time_s(mass_msun, v_frac_c, kappa)
    L = np.zeros_like(t_s)

    for i, t in enumerate(t_s):
        if t <= 0:
            continue
        tp = np.linspace(1e-3, t, n_integration)
        integrand = heating_rate(tp, mass_msun) * thermalization_efficiency(tp) * \
            np.exp((tp / td) ** 2) * (tp / td)
        integral = np.trapezoid(integrand, tp)
        L[i] = np.exp(-(t / td) ** 2) * integral / td

    return L, td


def bolometric_light_curve(t_days=None):
    """Total + per-component bolometric luminosity over the given time
    grid (days since merger). Returns a dict with 'time_days', 'total',
    and one array per component.
    """
    if t_days is None:
        t_days = np.geomspace(0.02, 20, 200)
    t_s = t_days * DAY_S

    out = {"time_days": t_days}
    total = np.zeros_like(t_s)
    diffusion_times = {}
    for name, p in COMPONENTS.items():
        L, td = component_luminosity(t_s, p["mass_msun"], p["v_frac_c"], p["kappa"])
        out[name] = L
        diffusion_times[name] = td / DAY_S
        total += L
    out["total"] = total
    out["diffusion_times_days"] = diffusion_times
    return out


def effective_temperature_k(L_erg_s, v_frac_c, t_days, sigma_sb_cgs=5.6704e-5):
    """Rough blackbody effective temperature from L = 4*pi*R^2*sigma*T^4,
    with photosphere radius approximated as R = v*t (homologous expansion).
    """
    t_s = t_days * DAY_S
    v_cm_s = v_frac_c * C_CGS
    R = v_cm_s * t_s
    R = np.maximum(R, 1e10)  # avoid div by ~0 at t->0
    T = (L_erg_s / (4 * np.pi * R ** 2 * sigma_sb_cgs)) ** 0.25
    return T


if __name__ == "__main__":
    lc = bolometric_light_curve()
    peak_idx = int(np.argmax(lc["total"]))
    print("AT2017gfo bolometric light curve (3-component Arnett model, Villar 2017 params)")
    print(f"  Peak luminosity: {lc['total'][peak_idx]:.3e} erg/s at t = {lc['time_days'][peak_idx]:.2f} days")
    print(f"  (published AT2017gfo peak: ~few x 10^41 erg/s within the first day -- order-of-magnitude check)")
    for name, td in lc["diffusion_times_days"].items():
        print(f"  {COMPONENTS[name]['label']:40s} diffusion time = {td:.2f} days")

    # color evolution: compare blue vs red component temperature at a few epochs
    print("\nEffective temperature by component (rough blackbody estimate):")
    for t_check in [0.5, 1.0, 3.0, 7.0, 14.0]:
        idx = int(np.argmin(np.abs(lc["time_days"] - t_check)))
        t_blue = effective_temperature_k(lc["blue"][idx], COMPONENTS["blue"]["v_frac_c"], lc["time_days"][idx])
        t_red = effective_temperature_k(lc["red"][idx], COMPONENTS["red"]["v_frac_c"], lc["time_days"][idx])
        print(f"  t={t_check:5.1f}d   blue T~{t_blue:7,.0f} K   red T~{t_red:7,.0f} K")
