"""
Act IV: how gold made it from neutron star mergers into the ground (and onto
a finger) on Earth.

Unlike physics.merger, physics.kilonova, and physics.rprocess, there is no
single fitted model here -- this is a well-established *qualitative*
sequence of events, not a differential equation. This module exists to give
that sequence concrete, sourced timestamps so it can be rendered as an
honest illustrative timeline rather than vague narration.

The sequence
------------
1. Enrichment: neutron star mergers across the universe's history (starting
   within the first ~100 million years, ongoing ever since) scatter
   r-process material -- including gold -- into the interstellar medium.
   By the time the solar nebula collapsed, ~9.2 billion years of this
   enrichment had already happened.
2. Solar system formation (t = 0 for the rest of this timeline): the
   protosolar nebula -- already enriched with r-process gold from countless
   prior mergers -- collapses to form the Sun and the protoplanetary disk,
   4.567 billion years ago (Pb-Pb dating of CAIs, the oldest solar system
   solids).
3. Core-mantle differentiation: within the first ~30-100 million years,
   Earth is molten enough that dense, "siderophile" (iron-loving) elements
   -- including nearly all of Earth's primordial gold -- sink with the iron
   into the core. If nothing else happened, the mantle and crust would be
   almost entirely gold-free.
4. The late veneer: after the core finishes forming, Earth continues to be
   struck by leftover planetesimals for roughly another 200 million years.
   This late bombardment adds a thin layer of fresh, undifferentiated
   material on top -- and its metal content is the standard explanation
   (Day, Pearson & Taylor 2007; reviewed in many places since) for why the
   mantle and crust contain any gold (and other siderophile elements) at
   all, in roughly the proportions observed.
5. Present day: that late-veneer gold, concentrated by billions of years of
   subsequent geology (hydrothermal veins, placer deposits), is what gets
   mined, refined, and shaped into the object worn at the end of this
   piece.

Sources
-------
Bouvier, A. & Wadhwa, M. (2010). "The age of the Solar System redefined by
    the oldest Pb-Pb age of a meteoritic inclusion." Nature Geoscience, 3,
    637-641. (4.567 Ga CAI age used for solar system formation)
Day, J. M. D., Pearson, D. G., & Taylor, L. A. (2007). "Highly Siderophile
    Element Constraints on Accretion and Differentiation of the
    Earth-Moon System." Science, 315, 217-219. (late veneer hypothesis)
Kleine, T. et al. (2009). "Hf-W chronology of the accretion and early
    evolution of asteroids and terrestrial planets." Geochimica et
    Cosmochimica Acta, 73, 5150-5188. (core formation timescale, ~30 Myr)
Johnson, J. A. (2019). "Populating the periodic table." Science, 363, 474.
    (r-process enrichment history feeding into solar system formation)
"""

# All times in millions of years (Myr). t=0 is solar system formation
# (CAI formation), matching standard cosmochemistry convention. Negative
# times are before solar system formation (the enrichment era); positive
# times are Earth's own history since.

SOLAR_SYSTEM_AGE_MYR = 4567.0          # Bouvier & Wadhwa 2010
FIRST_MERGERS_AFTER_BIG_BANG_MYR = 100.0  # earliest compact-binary mergers, illustrative
UNIVERSE_AGE_AT_SOLAR_SYSTEM_MYR = 13800.0 - 4567.0  # ~9.2 Gyr of prior enrichment

EVENTS = [
    {
        "t_myr": -(UNIVERSE_AGE_AT_SOLAR_SYSTEM_MYR - FIRST_MERGERS_AFTER_BIG_BANG_MYR),
        "label": "First neutron star mergers begin enriching the galaxy",
        "detail": "r-process material, including gold, starts entering the "
                   "interstellar medium within the universe's first ~100 Myr, "
                   "and continues for billions of years after.",
        "stage": "enrichment",
    },
    {
        "t_myr": -1.0,
        "label": "The gas cloud that becomes the Sun is already gold-enriched",
        "detail": "By the time the presolar nebula starts to collapse, ~9.2 "
                   "billion years of accumulated r-process enrichment is "
                   "already mixed into it.",
        "stage": "enrichment",
    },
    {
        "t_myr": 0.0,
        "label": "Solar system forms (t = 0)",
        "detail": "Pb-Pb dating of calcium-aluminum-rich inclusions (CAIs), "
                   "the oldest solar system solids, sets this at 4.567 "
                   "billion years ago.",
        "stage": "formation",
    },
    {
        "t_myr": 30.0,
        "label": "Earth differentiates: core forms",
        "detail": "Earth is hot and molten enough for dense, iron-loving "
                   "(siderophile) elements -- including nearly all "
                   "primordial gold -- to sink into the core.",
        "stage": "differentiation",
    },
    {
        "t_myr": 100.0,
        "label": "Moon-forming giant impact (context)",
        "detail": "A Mars-sized body strikes early Earth; the Moon forms "
                   "from the debris. Mentioned for timeline context, not "
                   "directly part of the gold story.",
        "stage": "context",
    },
    {
        "t_myr": 200.0,
        "label": "The late veneer: leftover planetesimals keep striking Earth",
        "detail": "After core formation is essentially complete, continued "
                   "bombardment by undifferentiated material adds a thin "
                   "layer of fresh metal -- including gold -- on top of the "
                   "already-differentiated mantle.",
        "stage": "late_veneer",
    },
    {
        "t_myr": 4567.0 - 4.567,  # ~ present day, offset only for display
        "label": "Present day: late-veneer gold reaches human hands",
        "detail": "Billions of years of geology (hydrothermal veins, placer "
                   "deposits) concentrate that late-veneer gold into "
                   "mineable form -- mined, refined, and shaped.",
        "stage": "present",
    },
]

STAGE_COLORS = {
    "enrichment": "#ffd35c",
    "formation": "#7ec8ff",
    "differentiation": "#ff6a3d",
    "context": "#4a5170",
    "late_veneer": "#6fd68a",
    "present": "#eef1fb",
}

STAGE_LABELS = {
    "enrichment": "Neutron star merger enrichment",
    "formation": "Solar system formation",
    "differentiation": "Core-mantle differentiation",
    "context": "Context (Moon formation)",
    "late_veneer": "Late veneer bombardment",
    "present": "Present day",
}


def timeline():
    """Return the event list, sorted by time."""
    return sorted(EVENTS, key=lambda e: e["t_myr"])


def summarize():
    ev = timeline()
    enrichment_span_gyr = (UNIVERSE_AGE_AT_SOLAR_SYSTEM_MYR - FIRST_MERGERS_AFTER_BIG_BANG_MYR) / 1000.0
    return {
        "solar_system_age_gyr": SOLAR_SYSTEM_AGE_MYR / 1000.0,
        "enrichment_span_before_solar_system_gyr": round(enrichment_span_gyr, 2),
        "core_formation_myr_after_t0": 30.0,
        "late_veneer_myr_after_t0": 200.0,
        "n_events": len(ev),
    }


if __name__ == "__main__":
    s = summarize()
    print("Gold's delivery to Earth -- illustrative timeline")
    print(f"  Solar system age: {s['solar_system_age_gyr']:.3f} Gyr")
    print(f"  Prior r-process enrichment before solar system formed: "
          f"~{s['enrichment_span_before_solar_system_gyr']} Gyr")
    print(f"  Core formation: ~{s['core_formation_myr_after_t0']:.0f} Myr after t=0")
    print(f"  Late veneer bombardment: ~{s['late_veneer_myr_after_t0']:.0f} Myr after t=0")
    print()
    for e in timeline():
        sign = "-" if e["t_myr"] < 0 else "+"
        print(f"  [{STAGE_LABELS[e['stage']]:32s}] t={sign}{abs(e['t_myr']):>9.1f} Myr   {e['label']}")
