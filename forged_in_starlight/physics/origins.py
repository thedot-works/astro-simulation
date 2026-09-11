"""
The periodic table, colored by astrophysical origin.

This is the classic "origin of the elements" classification popularized by
Jennifer Johnson (2019) and built on the framework Burbidge, Burbidge,
Fowler & Hoyle (1957) laid down: every element's dominant nucleosynthesis
channel, mapped onto its position in the periodic table. It is the
correctness-pass companion to physics.rprocess -- rprocess.py shows *how*
one r-process path climbs to gold; this module shows *where gold's origin
(neutron star mergers) sits relative to every other element's origin.

Categories used here (a standard simplification -- most elements have some
contribution from more than one channel; this assigns each its dominant
one):

  big_bang              hydrogen, helium, and trace lithium, made in the
                         first ~20 minutes after the Big Bang
  cosmic_ray_fission    lithium, beryllium, boron -- made by cosmic rays
                         fragmenting heavier nuclei in the interstellar
                         medium (spallation), not inside stars at all
  stellar_fusion        carbon through iron-group elements, built up by
                         hydrostatic nuclear fusion in stellar cores across
                         a star's life (low-mass and massive stars both
                         contribute different pieces of this range)
  exploding_massive_stars  iron-peak and some intermediate-mass elements
                         forged in the explosive shock of a core-collapse
                         supernova (silicon/alpha-process burning)
  exploding_white_dwarfs   a large share of the iron-peak elements
                         (particularly iron and nickel itself) come from
                         thermonuclear (Type Ia) supernovae, not
                         core-collapse ones
  dying_low_mass_stars  roughly half of everything heavier than iron,
                         built by slow neutron capture (s-process) in the
                         convective envelopes of asymptotic-giant-branch
                         stars
  merging_neutron_stars roughly the other half of everything heavier than
                         iron -- built by rapid neutron capture (r-process)
                         in the neutron-rich ejecta of neutron star
                         mergers (and possibly some rare supernovae).
                         Gold lives here.
  human_made            elements with no long-lived natural abundance,
                         only ever produced in reactors or accelerators

Sources
-------
Johnson, J. A. (2019). "Populating the periodic table: Nucleosynthesis of
    the elements." Science, 363(6426), 474-478. (the modern synthesis and
    the categorical scheme this module follows)
Burbidge, E. M., Burbidge, G. R., Fowler, W. A., & Hoyle, F. (1957).
    "Synthesis of the Elements in Stars." Rev. Mod. Phys., 29, 547.
Cameron, A. G. W. (1973). "Abundance of the Elements in the Solar System."
    Space Science Reviews, 15, 121. (an earlier version of the same map)
"""

GOLD_Z = 79

CATEGORY_COLORS = {
    "big_bang": "#8891ab",
    "cosmic_ray_fission": "#5ec9d8",
    "stellar_fusion": "#7ec8ff",
    "exploding_massive_stars": "#b98bff",
    "exploding_white_dwarfs": "#ff6a3d",
    "dying_low_mass_stars": "#6fd68a",
    "merging_neutron_stars": "#ffd35c",   # gold's color, and the r-process's
    "human_made": "#4a5170",
}

CATEGORY_LABELS = {
    "big_bang": "Big Bang nucleosynthesis",
    "cosmic_ray_fission": "Cosmic ray fission",
    "stellar_fusion": "Fusion in stars (hydrostatic burning)",
    "exploding_massive_stars": "Exploding massive stars (core-collapse)",
    "exploding_white_dwarfs": "Exploding white dwarfs (Type Ia)",
    "dying_low_mass_stars": "Dying low-mass stars (s-process)",
    "merging_neutron_stars": "Merging neutron stars (r-process)",
    "human_made": "Human-made",
}

# (Z, symbol, name, period, group, category)
# group is the standard 1-18 IUPAC column; lanthanides/actinides are drawn
# as two detached rows below the main table (period slots 8 and 9) at their
# usual f-block group offset, matching the conventional periodic table
# layout.
_ELEMENTS = [
    (1, "H", "Hydrogen", 1, 1, "big_bang"),
    (2, "He", "Helium", 1, 18, "big_bang"),
    (3, "Li", "Lithium", 2, 1, "cosmic_ray_fission"),
    (4, "Be", "Beryllium", 2, 2, "cosmic_ray_fission"),
    (5, "B", "Boron", 2, 13, "cosmic_ray_fission"),
    (6, "C", "Carbon", 2, 14, "stellar_fusion"),
    (7, "N", "Nitrogen", 2, 15, "stellar_fusion"),
    (8, "O", "Oxygen", 2, 16, "stellar_fusion"),
    (9, "F", "Fluorine", 2, 17, "stellar_fusion"),
    (10, "Ne", "Neon", 2, 18, "stellar_fusion"),
    (11, "Na", "Sodium", 3, 1, "stellar_fusion"),
    (12, "Mg", "Magnesium", 3, 2, "stellar_fusion"),
    (13, "Al", "Aluminium", 3, 13, "stellar_fusion"),
    (14, "Si", "Silicon", 3, 14, "stellar_fusion"),
    (15, "P", "Phosphorus", 3, 15, "exploding_massive_stars"),
    (16, "S", "Sulfur", 3, 16, "exploding_massive_stars"),
    (17, "Cl", "Chlorine", 3, 17, "exploding_massive_stars"),
    (18, "Ar", "Argon", 3, 18, "exploding_massive_stars"),
    (19, "K", "Potassium", 4, 1, "exploding_massive_stars"),
    (20, "Ca", "Calcium", 4, 2, "exploding_massive_stars"),
    (21, "Sc", "Scandium", 4, 3, "exploding_massive_stars"),
    (22, "Ti", "Titanium", 4, 4, "exploding_massive_stars"),
    (23, "V", "Vanadium", 4, 5, "exploding_white_dwarfs"),
    (24, "Cr", "Chromium", 4, 6, "exploding_white_dwarfs"),
    (25, "Mn", "Manganese", 4, 7, "exploding_white_dwarfs"),
    (26, "Fe", "Iron", 4, 8, "exploding_white_dwarfs"),
    (27, "Co", "Cobalt", 4, 9, "exploding_white_dwarfs"),
    (28, "Ni", "Nickel", 4, 10, "exploding_white_dwarfs"),
    (29, "Cu", "Copper", 4, 11, "dying_low_mass_stars"),
    (30, "Zn", "Zinc", 4, 12, "exploding_massive_stars"),
    (31, "Ga", "Gallium", 4, 13, "dying_low_mass_stars"),
    (32, "Ge", "Germanium", 4, 14, "dying_low_mass_stars"),
    (33, "As", "Arsenic", 4, 15, "merging_neutron_stars"),
    (34, "Se", "Selenium", 4, 16, "merging_neutron_stars"),
    (35, "Br", "Bromine", 4, 17, "merging_neutron_stars"),
    (36, "Kr", "Krypton", 4, 18, "merging_neutron_stars"),
    (37, "Rb", "Rubidium", 5, 1, "dying_low_mass_stars"),
    (38, "Sr", "Strontium", 5, 2, "dying_low_mass_stars"),
    (39, "Y", "Yttrium", 5, 3, "dying_low_mass_stars"),
    (40, "Zr", "Zirconium", 5, 4, "dying_low_mass_stars"),
    (41, "Nb", "Niobium", 5, 5, "dying_low_mass_stars"),
    (42, "Mo", "Molybdenum", 5, 6, "merging_neutron_stars"),
    (43, "Tc", "Technetium", 5, 7, "human_made"),
    (44, "Ru", "Ruthenium", 5, 8, "merging_neutron_stars"),
    (45, "Rh", "Rhodium", 5, 9, "merging_neutron_stars"),
    (46, "Pd", "Palladium", 5, 10, "merging_neutron_stars"),
    (47, "Ag", "Silver", 5, 11, "merging_neutron_stars"),
    (48, "Cd", "Cadmium", 5, 12, "merging_neutron_stars"),
    (49, "In", "Indium", 5, 13, "merging_neutron_stars"),
    (50, "Sn", "Tin", 5, 14, "dying_low_mass_stars"),
    (51, "Sb", "Antimony", 5, 15, "merging_neutron_stars"),
    (52, "Te", "Tellurium", 5, 16, "merging_neutron_stars"),
    (53, "I", "Iodine", 5, 17, "merging_neutron_stars"),
    (54, "Xe", "Xenon", 5, 18, "merging_neutron_stars"),
    (55, "Cs", "Caesium", 6, 1, "merging_neutron_stars"),
    (56, "Ba", "Barium", 6, 2, "dying_low_mass_stars"),
    (57, "La", "Lanthanum", 8, 3, "dying_low_mass_stars"),
    (58, "Ce", "Cerium", 8, 4, "dying_low_mass_stars"),
    (59, "Pr", "Praseodymium", 8, 5, "dying_low_mass_stars"),
    (60, "Nd", "Neodymium", 8, 6, "dying_low_mass_stars"),
    (61, "Pm", "Promethium", 8, 7, "human_made"),
    (62, "Sm", "Samarium", 8, 8, "merging_neutron_stars"),
    (63, "Eu", "Europium", 8, 9, "merging_neutron_stars"),
    (64, "Gd", "Gadolinium", 8, 10, "merging_neutron_stars"),
    (65, "Tb", "Terbium", 8, 11, "merging_neutron_stars"),
    (66, "Dy", "Dysprosium", 8, 12, "merging_neutron_stars"),
    (67, "Ho", "Holmium", 8, 13, "merging_neutron_stars"),
    (68, "Er", "Erbium", 8, 14, "merging_neutron_stars"),
    (69, "Tm", "Thulium", 8, 15, "merging_neutron_stars"),
    (70, "Yb", "Ytterbium", 8, 16, "dying_low_mass_stars"),
    (71, "Lu", "Lutetium", 8, 17, "dying_low_mass_stars"),
    (72, "Hf", "Hafnium", 6, 4, "dying_low_mass_stars"),
    (73, "Ta", "Tantalum", 6, 5, "merging_neutron_stars"),
    (74, "W", "Tungsten", 6, 6, "dying_low_mass_stars"),
    (75, "Re", "Rhenium", 6, 7, "merging_neutron_stars"),
    (76, "Os", "Osmium", 6, 8, "merging_neutron_stars"),
    (77, "Ir", "Iridium", 6, 9, "merging_neutron_stars"),
    (78, "Pt", "Platinum", 6, 10, "merging_neutron_stars"),
    (79, "Au", "Gold", 6, 11, "merging_neutron_stars"),
    (80, "Hg", "Mercury", 6, 12, "merging_neutron_stars"),
    (81, "Tl", "Thallium", 6, 13, "dying_low_mass_stars"),
    (82, "Pb", "Lead", 6, 14, "dying_low_mass_stars"),
    (83, "Bi", "Bismuth", 6, 15, "dying_low_mass_stars"),
    (84, "Po", "Polonium", 6, 16, "human_made"),
    (85, "At", "Astatine", 6, 17, "human_made"),
    (86, "Rn", "Radon", 6, 18, "human_made"),
    (87, "Fr", "Francium", 7, 1, "human_made"),
    (88, "Ra", "Radium", 7, 2, "merging_neutron_stars"),
    (89, "Ac", "Actinium", 9, 3, "human_made"),
    (90, "Th", "Thorium", 9, 4, "merging_neutron_stars"),
    (91, "Pa", "Protactinium", 9, 5, "human_made"),
    (92, "U", "Uranium", 9, 6, "merging_neutron_stars"),
    (93, "Np", "Neptunium", 9, 7, "human_made"),
    (94, "Pu", "Plutonium", 9, 8, "human_made"),
    (95, "Am", "Americium", 9, 9, "human_made"),
    (96, "Cm", "Curium", 9, 10, "human_made"),
    (97, "Bk", "Berkelium", 9, 11, "human_made"),
    (98, "Cf", "Californium", 9, 12, "human_made"),
    (99, "Es", "Einsteinium", 9, 13, "human_made"),
    (100, "Fm", "Fermium", 9, 14, "human_made"),
    (101, "Md", "Mendelevium", 9, 15, "human_made"),
    (102, "No", "Nobelium", 9, 16, "human_made"),
    (103, "Lr", "Lawrencium", 9, 17, "human_made"),
]


def elements():
    """Return the element table as a list of dicts."""
    out = []
    for z, sym, name, period, group, category in _ELEMENTS:
        out.append({
            "Z": z,
            "symbol": sym,
            "name": name,
            "period": period,
            "group": group,
            "category": category,
            "color": CATEGORY_COLORS[category],
            "is_gold": z == GOLD_Z,
        })
    return out


def category_counts():
    counts = {}
    for e in elements():
        counts[e["category"]] = counts.get(e["category"], 0) + 1
    return counts


if __name__ == "__main__":
    counts = category_counts()
    total = sum(counts.values())
    print(f"Origin of the elements -- {total} elements classified (Z=1-103)\n")
    for cat, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {CATEGORY_LABELS[cat]:45s} {n:3d} elements")
    gold = next(e for e in elements() if e["is_gold"])
    print(f"\nGold (Z=79): {CATEGORY_LABELS[gold['category']]}")
