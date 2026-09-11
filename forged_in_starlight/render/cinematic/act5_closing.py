"""
Section 5 -- Summary.

A results summary, in the register of a conclusion slide: the measured
values from each section, compared to their published/theoretical
references, plus the periodic-table origin classification restated as a
category count. No illustrative closing imagery.

Render:
    python -m manim -qm render/cinematic/act5_closing.py Act5Closing
"""

from render.cinematic.common import *


class Act5Closing(Scene):
    def construct(self):
        self.camera.background_color = BG
        data = load_data()

        header = section_title("5", "Summary of results")
        self.play(FadeIn(header), run_time=0.5)

        mc_meas = data["chirp_mass_measured"]
        mc_std = data["chirp_mass_measured_std"]
        mc_pub = data["chirp_mass_published"]
        gold = data["gold"]
        path = data["rprocess_path"]
        final = path[-1]

        rows = [
            ("Chirp mass (H1 strain, this analysis)", f"{mc_meas:.3f} ± {mc_std:.3f} M☉"),
            ("Chirp mass (Abbott et al. 2017, published)", f"{mc_pub:.3f} M☉"),
            ("r-process network final nucleus", f"Z={final['Z']}, N={final['N']} (A={final['Z']+final['N']})"),
            ("Target: gold (Au-197)", f"Z={gold['Z']}, N={gold['N']} (A={gold['A']})"),
            ("Network reaches target exactly", "True" if (final["Z"], final["N"]) == (gold["Z"], gold["N"]) else "False"),
        ]

        table = VGroup()
        for label, value in rows:
            row = VGroup(
                Text(label, font_size=20, color=DIM),
                Text(value, font_size=20, color=INK, weight=BOLD),
            )
            row.arrange(RIGHT, buff=0.4)
            table.add(row)
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        table.move_to(UP * 1.15)

        self.play(LaggedStart(*[FadeIn(r) for r in table], lag_ratio=0.15), run_time=1.6)
        self.wait(1.5)

        counts_data = data["category_labels"]
        els = data["elements"]
        from collections import Counter
        counts = Counter(e["category"] for e in els)

        cats = ["merging_neutron_stars", "dying_low_mass_stars", "exploding_massive_stars",
                "exploding_white_dwarfs", "stellar_fusion", "cosmic_ray_fission", "big_bang", "human_made"]
        left_cats, right_cats = cats[:4], cats[4:]

        def make_column(cat_list):
            col = VGroup(*[
                Text(f"{counts_data[c]}: {counts[c]} elements", font_size=16, color=DIM)
                for c in cat_list
            ])
            col.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            return col

        left_col = make_column(left_cats)
        right_col = make_column(right_cats)
        columns = VGroup(left_col, right_col).arrange(RIGHT, aligned_edge=UP, buff=0.6)
        if columns.width > 10.6:
            columns.set_width(10.6)

        count_header = Text("Element-origin classification (Z = 1-103):", font_size=18, color=INK)
        count_header.next_to(table, DOWN, buff=0.35).align_to(table, LEFT)
        columns.next_to(count_header, DOWN, buff=0.2).align_to(table, LEFT)

        self.play(FadeIn(count_header), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(c) for c in [*left_col, *right_col]], lag_ratio=0.06), run_time=1.2)
        self.wait(1.6)

        note = source_note("Full source list and validation instructions: README.md")
        self.play(FadeIn(note), run_time=0.4)
        self.wait(1.4)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
