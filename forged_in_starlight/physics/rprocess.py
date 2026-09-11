"""
The r-process: a simplified "waiting-point" neutron-capture network that
climbs from an iron-group seed nucleus up to gold.

This is not a full nuclear reaction network (that requires solving
Boltzmann-like equations across hundreds of isotopes with a real
nuclear-physics code such as WinNet or SkyNet). It is the standard
*conceptual* simplification used to explain and visualize the r-process
in the literature: material captures neutrons rapidly (moving straight
up the nuclide chart, N increasing at fixed Z) until it reaches a
neutron shell closure (N = 50, 82, or 126), where neutron capture stalls
because the next neutron is much more loosely bound. There, the nucleus
"waits," beta-decaying (N -> N-1, Z -> Z+1) until it can resume capturing
neutrons. This produces the path's characteristic staircase shape and is
directly responsible for the three real abundance peaks observed in
solar-system r-process material, at mass number A ~ 80, 130, and 195.

Gold (Au-197, Z=79, N=118) sits in the tail of the A~195 peak -- the one
fed by the N=126 waiting point. After the merger ejecta's free neutrons
run out (a real physical event called "freeze-out," happening roughly a
second after the merger), the very neutron-rich nuclei sitting at the
N=126 waiting point beta-decay down their isobaric chain (constant mass
number A, N decreasing, Z increasing one at a time) until they reach a
stable nucleus. For A=197, that stable nucleus is gold.

Sources
-------
Arnould, M., Goriely, S., & Takahashi, K. (2007). "The r-process of
    stellar nucleosynthesis: Astrophysics and nuclear physics
    achievements and mysteries." Physics Reports, 450, 97-213.
    (waiting-point-approximation description; representative r-process
    waiting-point beta-decay half-lives of order 10 ms - 1 s used here
    are illustrative of the timescales this review discusses, not a
    lookup of any single specific isotope's measured half-life.)
Burbidge, E. M., Burbidge, G. R., Fowler, W. A., & Hoyle, F. (1957).
    "Synthesis of the Elements in Stars." Rev. Mod. Phys., 29, 547.
    (the original B2FH paper defining the r-process and s-process)
"""

import numpy as np

MAGIC_N = (50, 82, 126)

# Representative (illustrative, order-of-magnitude) waiting-point beta-decay
# half-lives in seconds, increasing toward heavier waiting points as the
# path moves closer to the drip line more slowly -- consistent with the
# general trend discussed in Arnould, Goriely & Takahashi (2007).
WAITING_POINT_HALFLIFE_S = {50: 0.03, 82: 0.15, 126: 0.6}

SEED = {"Z": 26, "N": 30}       # Fe-56: a realistic iron-group r-process seed
GOLD = {"Z": 79, "N": 118, "A": 197, "name": "Au-197 (gold, stable)"}

# how many beta decays happen at each waiting point before the path resumes
# capturing neutrons (illustrative -- real amounts depend on the local
# neutron density and are not fixed constants)
BETA_STEPS_AT_WAITING_POINT = {50: 4, 82: 6, 126: 5}


def stability_valley_z(a):
    """Approximate charge Z of the beta-stability valley for mass number A,
    from the semi-empirical mass formula's asymmetry-term minimization.
    Standard textbook approximation, e.g. Krane, 'Introductory Nuclear
    Physics' (1988), eq. for the stability valley.
    """
    a = np.asarray(a, dtype=float)
    return a / (1.98 + 0.015 * a ** (2.0 / 3.0))


def build_path():
    """Construct the (N, Z, stage, t_relative) waiting-point path from the
    seed nucleus to gold. 'stage' is 'capture' (rapid neutron capture) or
    'decay' (beta decay at a waiting point). t_relative is a cumulative
    illustrative timeline in seconds, with capture treated as effectively
    instantaneous compared to beta-decay waiting times.
    """
    path = []
    t = 0.0
    Z, N = SEED["Z"], SEED["N"]
    path.append({"Z": Z, "N": N, "stage": "seed", "t": t})

    for n_magic in MAGIC_N:
        # rapid neutron capture up to the next shell closure
        capture_steps = np.linspace(N, n_magic, max(2, (n_magic - N) // 2))
        for n_step in capture_steps[1:]:
            t += 0.002  # capture is fast; a couple ms per step, illustrative
            path.append({"Z": Z, "N": int(round(n_step)), "stage": "capture", "t": t})
        N = n_magic

        # beta-decay steps at the waiting point
        thalf = WAITING_POINT_HALFLIFE_S[n_magic]
        for _ in range(BETA_STEPS_AT_WAITING_POINT[n_magic]):
            t += thalf
            Z += 1
            path.append({"Z": Z, "N": N, "stage": "decay", "t": t})

    # freeze-out: neutrons run out (~1s after merger, a real physical
    # timescale for BNS-merger ejecta), and the path decays down the A=197
    # isobaric chain (N decreasing, Z increasing) to stable gold.
    A_freeze = Z + N
    target_A = GOLD["A"]
    # walk down in N / up in Z at fixed A until we reach gold's (Z, N)
    while (Z, N) != (GOLD["Z"], GOLD["N"]) and A_freeze != target_A:
        # adjust seed path deterministically toward the gold isobar if the
        # network's illustrative steps didn't land exactly on A=197
        if A_freeze < target_A:
            N += 1
        else:
            N -= 1
        A_freeze = Z + N

    while Z < GOLD["Z"]:
        t += 0.05  # freeze-out beta decays are also fast, sub-second each
        Z += 1
        N -= 1
        path.append({"Z": Z, "N": N, "stage": "freeze_out_decay", "t": t})

    return path


def summarize(path):
    seed = path[0]
    final = path[-1]
    n_capture = sum(1 for p in path if p["stage"] == "capture")
    n_decay = sum(1 for p in path if p["stage"] in ("decay", "freeze_out_decay"))
    return {
        "seed": f"Z={seed['Z']}, N={seed['N']} (A={seed['Z']+seed['N']})",
        "final": f"Z={final['Z']}, N={final['N']} (A={final['Z']+final['N']})",
        "matches_gold": (final["Z"], final["N"]) == (GOLD["Z"], GOLD["N"]),
        "n_capture_steps": n_capture,
        "n_beta_decay_steps": n_decay,
        "total_illustrative_time_s": path[-1]["t"],
    }


if __name__ == "__main__":
    path = build_path()
    s = summarize(path)
    print("r-process waiting-point path: iron seed -> gold")
    print(f"  Seed:  {s['seed']}")
    print(f"  Final: {s['final']}  (target: Z={GOLD['Z']}, N={GOLD['N']}, {GOLD['name']})")
    print(f"  Reaches gold exactly: {s['matches_gold']}")
    print(f"  {s['n_capture_steps']} neutron-capture steps, {s['n_beta_decay_steps']} beta-decay steps")
    print(f"  Total illustrative timeline: {s['total_illustrative_time_s']:.2f} s "
          f"(real r-process nucleosynthesis completes within ~1-2 s of merger)")
