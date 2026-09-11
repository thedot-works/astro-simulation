"""
Section 4 -- Delivery of r-process material to Earth.

A direct animation of physics.earth_delivery's sourced timeline: events
appear in temporal order along a compressed axis (necessarily compressed,
since it spans ~9.1 Gyr of pre-solar enrichment down to a ~200 Myr window
of Earth's early history), each labeled with its stage and its published
source. No illustrative imagery (no planet graphic, no mining icon) --
each event is a labeled point on a timeline, the same register as
render/earth_timeline.py's correctness-pass figure.

Render:
    python -m manim -qm render/cinematic/act4_earth.py Act4Earth
"""

from render.cinematic.common import *


class Act4Earth(Scene):
    def construct(self):
        self.camera.background_color = BG
        data = load_data()
        events = sorted(data["earth_timeline"], key=lambda e: e["t_myr"])
        colors = data["stage_colors"]

        header = section_title("4", "Delivery of r-process material to Earth",
                                 "Illustrative timeline from published cosmochemical constraints")
        self.play(FadeIn(header), run_time=0.5)

        note = source_note("Bouvier & Wadhwa (2010); Kleine et al. (2009); Day, Pearson & Taylor (2007)")
        self.play(FadeIn(note), run_time=0.4)

        scale_cap = caption("Axis position is by event order, not linear time (span: ~9.1 Gyr to ~200 Myr)",
                              y=2.3, scale=0.4)
        self.play(FadeIn(scale_cap), run_time=0.5)

        n = len(events)
        xs = np.linspace(-5.6, 5.6, n)
        y = 0.3
        line = Line(np.array([-5.9, y, 0]), np.array([5.9, y, 0]), color=FAINT, stroke_width=1.5)
        self.play(Create(line), run_time=0.6)

        dots, labels, t_labels = [], [], []
        for i, (x, e) in enumerate(zip(xs, events)):
            c = colors[e["stage"]]
            d = Dot(np.array([x, y, 0]), radius=0.09, color=c)
            lbl = Text(e["label"], font_size=16, color=c)
            lbl.set_width(min(lbl.width, 2.3))
            lbl.next_to(d, UP if i % 2 == 0 else DOWN, buff=0.3)
            t_sign = "-" if e["t_myr"] < 0 else "+"
            t_lbl = Text(f"t = {t_sign}{abs(e['t_myr']):.0f} Myr", font_size=13, color=DIM)
            t_lbl.next_to(lbl, UP if i % 2 == 0 else DOWN, buff=0.08)
            dots.append(d)
            labels.append(lbl)
            t_labels.append(t_lbl)

        for d, lbl, tl in zip(dots, labels, t_labels):
            self.play(FadeIn(d, scale=1.2), FadeIn(lbl), FadeIn(tl), run_time=0.5)

        self.wait(1.0)

        # a single marker traces the sequence, left to right, as a
        # continuity device -- not a narrative "particle", just a cursor
        cursor = Dot(dots[0].get_center(), radius=0.05, color=GOLD)
        self.play(FadeIn(cursor), run_time=0.3)
        travel_path = VMobject()
        travel_path.set_points_as_corners([d.get_center() for d in dots])
        self.play(MoveAlongPath(cursor, travel_path), run_time=2.5, rate_func=linear)
        self.play(FadeOut(cursor), run_time=0.3)

        sub = caption(
            "r-process ejecta enriches the interstellar medium; the solar nebula forms already enriched; "
            "core-mantle differentiation removes primordial siderophiles; the late veneer resupplies the mantle.",
            y=-3.6, scale=0.42)
        self.play(FadeIn(sub), run_time=0.6)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
