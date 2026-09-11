"""
Section 3 -- GW170817 and the r-process.

Three quantitative beats, each a direct plot of real or physics-derived
data (no illustrative substitutes): (1) the real whitened H1 strain around
the merger, with the rising-frequency chirp visible directly in the time
series; (2) the measured chirp mass, obtained from a sliding-window
frequency ridge fit to that same real data, plotted against the analytic
post-Newtonian frequency track and compared numerically to the published
LIGO/Virgo value; (3) the r-process waiting-point network on a nuclide
chart, from physics.rprocess, landing exactly on Au-197.

Render:
    python -m manim -qm render/cinematic/act3_rprocess.py Act3RProcess
"""

from render.cinematic.common import *


class Act3RProcess(Scene):
    def construct(self):
        self.camera.background_color = BG
        data = load_data()

        header = section_title("3", "GW170817 and the r-process",
                                 "Neutron star merger data and the nucleosynthesis path to gold")
        self.play(FadeIn(header), run_time=0.5)

        # --- beat 1: real whitened strain, the chirp visible directly ---
        wt = np.array(data["waveform_t_before_merger"])
        wy = np.array(data["waveform_strain_normalized"])

        wf_axes = Axes(
            x_range=[wt.min(), wt.max(), 0.1], y_range=[-1.2, 1.2, 0.5],
            x_length=9.5, y_length=3.2,
            axis_config={"color": DIM, "stroke_width": 1.3}, tips=False,
        ).shift(UP * 1.1)
        add_axis_numbers(wf_axes, font_size=14, num_decimal_places=1)
        wf_xlab = Text("Time relative to merger (s)", font_size=18, color=DIM).next_to(wf_axes, DOWN, buff=0.45)
        wf_ylab = Text("Whitened strain (normalized)", font_size=16, color=DIM).rotate(PI / 2).next_to(wf_axes.y_axis, RIGHT, buff=0.55)

        self.play(Create(wf_axes), FadeIn(wf_xlab), FadeIn(wf_ylab), run_time=0.9)

        wf_points = [wf_axes.c2p(t, y) for t, y in zip(wt, wy)]
        wf_curve = VMobject(color=CAPTURE_COLOR, stroke_width=1.5)
        wf_curve.set_points_as_corners(wf_points)

        cap1 = caption("LIGO Hanford (H1) strain, whitened and bandpassed 30-400 Hz", y=-1.75, scale=0.5)
        self.play(FadeIn(cap1), run_time=0.4)
        self.play(Create(wf_curve), run_time=3.5, rate_func=linear)

        merger_line = DashedLine(wf_axes.c2p(0, -1.2), wf_axes.c2p(0, 1.2), color=GOLD, stroke_width=2.0)
        merger_lbl = Text("t = 0 (merger)", font_size=16, color=GOLD).next_to(merger_line, UP, buff=0.15)
        self.play(Create(merger_line), FadeIn(merger_lbl), run_time=0.6)
        self.wait(1.0)

        note1 = source_note("GW170817, H1 strain: GWOSC / LIGO-Virgo (Abbott et al. 2017)")
        self.play(FadeIn(note1), run_time=0.4)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in [wf_axes, wf_xlab, wf_ylab, wf_curve, cap1,
                                            merger_line, merger_lbl, note1]], run_time=0.6)

        # --- beat 2: measured chirp mass vs. published, with the PN fit ---
        rt = np.array(data["ridge_t_before_merger"])
        rf = np.array(data["ridge_f_gw"])
        ft = np.array(data["fit_t_before_merger"])
        ff = np.array(data["fit_f_gw"])

        cm_axes = Axes(
            x_range=[0, float(rt.max()) * 1.05, 0.4], y_range=[0, 400, 100],
            x_length=8.6, y_length=3.6,
            axis_config={"color": DIM, "stroke_width": 1.3}, tips=False,
        ).shift(UP * 0.15 + RIGHT * 0.4)
        add_axis_numbers(cm_axes, font_size=15, num_decimal_places=1)
        cm_xlab = Text("Time before merger (s)", font_size=18, color=DIM).next_to(cm_axes.x_axis, DOWN, buff=0.4)
        cm_ylab = Text("GW frequency (Hz)", font_size=18, color=DIM).rotate(PI / 2).next_to(cm_axes.y_axis, LEFT, buff=0.5)

        cap2 = caption("Frequency ridge from a sliding-window periodogram of the same H1 data", y=2.42, scale=0.42)
        self.play(Create(cm_axes), FadeIn(cm_xlab), FadeIn(cm_ylab), run_time=0.9)
        self.play(FadeIn(cap2), run_time=0.4)

        ridge_dots = VGroup(*[Dot(cm_axes.c2p(t, f), radius=0.035, color=INK) for t, f in zip(rt, rf)])
        self.play(LaggedStart(*[FadeIn(d) for d in ridge_dots], lag_ratio=0.02), run_time=1.2)

        fit_points = [cm_axes.c2p(t, f) for t, f in zip(ft, ff) if f <= 400]
        fit_curve = VMobject(color=GOLD, stroke_width=2.5)
        fit_curve.set_points_smoothly(fit_points)
        self.play(Create(fit_curve), run_time=1.2)

        mc_meas = data["chirp_mass_measured"]
        mc_std = data["chirp_mass_measured_std"]
        mc_pub = data["chirp_mass_published"]
        result = VGroup(
            Text(f"Measured chirp mass: {mc_meas:.3f} +/- {mc_std:.3f} Msun", font_size=18, color=INK),
            Text(f"Published (Abbott et al. 2017): {mc_pub:.3f} Msun", font_size=18, color=GOLD),
        ).arrange(DOWN, aligned_edge=ORIGIN, buff=0.12)
        result.next_to(cm_xlab, DOWN, buff=0.3)
        self.play(FadeIn(result), run_time=0.7)
        self.wait(1.8)

        self.play(*[FadeOut(m) for m in [cm_axes, cm_xlab, cm_ylab, cap2, ridge_dots,
                                            fit_curve, result]], run_time=0.7)

        # --- beat 3: the r-process network on a nuclide chart ---
        path = data["rprocess_path"]
        gold = data["gold"]
        seed = data["seed"]
        magic_n = data["magic_n"]

        n_min, n_max = 20, 165
        z_min, z_max = 15, 90
        axes = Axes(
            x_range=[n_min, n_max, 20], y_range=[z_min, z_max, 15],
            x_length=9.0, y_length=4.2,
            axis_config={"color": DIM, "stroke_width": 1.3}, tips=False,
        ).shift(DOWN * 0.3)
        add_axis_numbers(axes, font_size=15)
        xlab = Text("Neutron number, N", font_size=20, color=DIM).next_to(axes.x_axis, DOWN, buff=0.25)
        ylab = Text("Proton number, Z", font_size=20, color=DIM).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.3)

        chart_cap = caption("Waiting-point r-process network (physics.rprocess)", y=2.42, scale=0.42)
        self.play(Create(axes), FadeIn(xlab), FadeIn(ylab), run_time=0.9)
        self.play(FadeIn(chart_cap), run_time=0.5)

        for nm in magic_n:
            if nm <= n_max:
                line = DashedLine(axes.c2p(nm, z_min), axes.c2p(nm, z_max), color=FAINT, stroke_width=1.3)
                lbl = Text(f"N={nm}", font_size=15, color=DIM).next_to(line, UP, buff=0.05)
                self.play(FadeIn(line), FadeIn(lbl), run_time=0.25)

        seed_pt = axes.c2p(seed["N"], seed["Z"])
        gold_pt = axes.c2p(gold["N"], gold["Z"])
        seed_dot = Circle(radius=0.08, color=INK, stroke_width=2).move_to(seed_pt)
        seed_label = Text("Fe-56 (seed)", font_size=17, color=INK).next_to(seed_pt, DOWN, buff=0.15)
        gold_marker = Square(side_length=0.2, color=GOLD, stroke_width=2.5).move_to(gold_pt)
        gold_label = Text("Au-197 (stable)", font_size=18, color=GOLD).next_to(gold_pt, RIGHT, buff=0.2)

        self.play(FadeIn(seed_dot), FadeIn(seed_label), run_time=0.4)
        self.play(FadeIn(gold_marker), FadeIn(gold_label), run_time=0.4)

        moving_dot = Dot(seed_pt, radius=0.06, color=INK)
        self.add(moving_dot)

        batch = 3
        for i in range(0, len(path) - 1, batch):
            segs = VGroup()
            j_end = min(i + batch, len(path) - 1)
            for j in range(i, j_end):
                p0 = axes.c2p(path[j]["N"], path[j]["Z"])
                p1 = axes.c2p(path[j + 1]["N"], path[j + 1]["Z"])
                stage = path[j + 1]["stage"]
                color = DECAY_COLOR if "decay" in stage else CAPTURE_COLOR
                segs.add(Line(p0, p1, color=color, stroke_width=2.0))
            end_pt = axes.c2p(path[j_end]["N"], path[j_end]["Z"])
            self.play(Create(segs), moving_dot.animate.move_to(end_pt), run_time=0.1, rate_func=linear)

        self.play(moving_dot.animate.set_color(GOLD), run_time=0.4)

        legend = VGroup(
            Line(ORIGIN, RIGHT * 0.4, color=CAPTURE_COLOR, stroke_width=3),
            Text("neutron capture", font_size=16, color=DIM),
            Line(ORIGIN, RIGHT * 0.4, color=DECAY_COLOR, stroke_width=3),
            Text("beta decay", font_size=16, color=DIM),
        )
        legend[1].next_to(legend[0], RIGHT, buff=0.1)
        legend[2].next_to(legend[1], RIGHT, buff=0.3)
        legend[3].next_to(legend[2], RIGHT, buff=0.1)
        legend.arrange(RIGHT, buff=0.15)
        legend.to_corner(DR, buff=0.5).shift(UP * 1.5)
        self.play(FadeIn(legend), run_time=0.4)

        gold_cap = caption(
            "Freeze-out decay along A = 197 terminates at the stable nucleus Au-197.",
            y=-3.5, scale=0.5)
        note = source_note("Waiting-point half-lives: Arnould, Goriely & Takahashi (2007)")
        self.play(FadeIn(gold_cap), FadeIn(note), run_time=0.5)
        self.wait(1.4)

        other_cap = caption(
            "The same rapid-capture process also produces Ag, Pt, and U -- classified in physics.origins.",
            y=-3.5, scale=0.5)
        self.play(FadeOut(gold_cap), FadeIn(other_cap), run_time=0.5)
        self.wait(1.4)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
