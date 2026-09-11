"""
Section 2 -- The binding-energy limit at iron.

Fusion releases energy only while climbing the binding-energy-per-nucleon
curve; past iron, fusing two nuclei costs energy rather than releasing it.
This section plots that curve from standard published nuclear data for a
representative set of nuclides and marks the peak explicitly.

Binding energy per nucleon (MeV), standard published values (e.g. Krane,
"Introductory Nuclear Physics"):
    H-1: 0.0, He-4: 7.07, C-12: 7.68, O-16: 7.98, Si-28: 8.45,
    Ca-40: 8.55, Fe-56: 8.79 (peak), Ni-62: 8.79,
    Kr-84: 8.72, Sn-120: 8.50, Xe-136: 8.40, Pb-208: 7.87, U-238: 7.57

Render:
    python -m manim -qm render/cinematic/act2_wall.py Act2Wall
"""

from render.cinematic.common import *

NUCLIDES = [
    ("H-1", 1, 0.0), ("He-4", 4, 7.07), ("C-12", 12, 7.68), ("O-16", 16, 7.98),
    ("Si-28", 28, 8.45), ("Ca-40", 40, 8.55), ("Fe-56", 56, 8.79),
    ("Ni-62", 62, 8.79), ("Kr-84", 84, 8.72), ("Sn-120", 120, 8.50),
    ("Xe-136", 136, 8.40), ("Pb-208", 208, 7.87), ("U-238", 238, 7.57),
]


class Act2Wall(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = section_title("2", "The binding-energy limit",
                                 "Average binding energy per nucleon vs. mass number")
        self.play(FadeIn(header), run_time=0.5)

        axes = Axes(
            x_range=[0, 240, 40], y_range=[0, 9.5, 2],
            x_length=8.6, y_length=4.6,
            axis_config={"color": DIM, "stroke_width": 1.5},
            tips=False,
        ).shift(DOWN * 0.15 + RIGHT * 0.5)
        add_axis_numbers(axes, font_size=16)
        x_label = Text("Mass number, A", font_size=22, color=DIM).next_to(axes.x_axis.numbers, DOWN, buff=0.25)
        y_label = Text("Binding energy / nucleon (MeV)", font_size=17, color=DIM)
        y_label.rotate(PI / 2).next_to(axes.y_axis.numbers, LEFT, buff=0.25)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.0)

        points = [axes.c2p(a, be) for _, a, be in NUCLIDES]
        curve = VMobject(color=CAPTURE_COLOR, stroke_width=3.0)
        curve.set_points_smoothly(points)

        dots = VGroup(*[Dot(p, radius=0.05, color=INK) for p in points])
        labels = VGroup(*[
            Text(name, font_size=15, color=DIM).next_to(p, UP, buff=0.1)
            for (name, _, _), p in zip(NUCLIDES, points)
        ])

        self.play(Create(curve), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.05), run_time=0.8)

        fe_idx = [n[0] for n in NUCLIDES].index("Fe-56")
        fe_point = points[fe_idx]
        fe_dot = Dot(fe_point, radius=0.09, color=GOLD)
        fe_ring = Circle(radius=0.18, color=GOLD, stroke_width=2).move_to(fe_point)
        fe_label = Text("Fe-56 (peak, 8.79 MeV/nucleon)", font_size=20, color=GOLD)
        fe_label.next_to(fe_point, UP, buff=0.4)

        self.play(FadeIn(fe_dot), Create(fe_ring), FadeIn(fe_label), run_time=0.7)

        left_txt = Text("fusion releases energy", font_size=18, color=CAPTURE_COLOR)
        left_txt.move_to(axes.c2p(45, 3.0))
        left_arrow = Arrow(left_txt.get_top() + UP * 0.05, axes.c2p(35, 6.2), color=CAPTURE_COLOR, buff=0.1, stroke_width=2.5)

        right_txt = Text("fusion costs energy", font_size=18, color=DECAY_COLOR)
        right_txt.move_to(axes.c2p(195, 5.2))
        right_arrow = Arrow(right_txt.get_top() + UP * 0.05, axes.c2p(200, 7.9), color=DECAY_COLOR, buff=0.1, stroke_width=2.5)

        self.play(FadeIn(left_txt), GrowArrow(left_arrow), run_time=0.6)
        self.play(FadeIn(right_txt), GrowArrow(right_arrow), run_time=0.6)
        self.wait(0.6)

        cap = caption("Beyond A ~ 56-62, hydrostatic fusion is no longer exothermic.", y=-3.55, scale=0.5)
        note = source_note("Binding-energy values: Krane, Introductory Nuclear Physics")
        self.play(FadeIn(cap), FadeIn(note), run_time=0.6)
        self.wait(1.4)

        sub = caption("The elements heavier than the iron peak require a different formation channel.",
                       y=-3.55, scale=0.5)
        self.play(FadeOut(cap), FadeIn(sub), run_time=0.5)
        self.wait(1.4)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
