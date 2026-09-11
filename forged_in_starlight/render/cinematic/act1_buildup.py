"""
Section 1 -- Nucleosynthetic origin of the elements up to the iron peak.

A periodic table, laid out in standard IUPAC group/period form, filled in
category by category in the order each formation channel became active in
cosmic history. This is a direct animation of physics.origins's
classification (Z=1-103, eight formation channels) -- no invented imagery,
no narrative framing beyond stating which physical process is responsible
for which elements and when.

Render:
    python -m manim -qm render/cinematic/act1_buildup.py Act1Buildup
"""

from render.cinematic.common import *

CATEGORY_ORDER_ACT1 = ["big_bang", "cosmic_ray_fission", "stellar_fusion",
                       "exploding_massive_stars", "exploding_white_dwarfs"]
CELL = 0.30


def cell_xy(period, group):
    x = (group - 9.5) * CELL * 1.05
    if period <= 7:
        y = (3.6 - period) * CELL * 1.05
    else:
        y = (3.6 - 7 - 1.3 - (period - 8)) * CELL * 1.05
    return x, y


class Act1Buildup(Scene):
    def construct(self):
        self.camera.background_color = BG
        data = load_data()
        els = data["elements"]
        colors = data["category_colors"]

        header = section_title("1", "Nucleosynthetic origin of the elements",
                                 "Classification of Z = 1-103 by dominant formation process (Johnson 2019)")
        self.play(FadeIn(header), run_time=0.6)

        squares, symbols = {}, {}
        for e in els:
            x, y = cell_xy(e["period"], e["group"])
            sq = Square(side_length=CELL, stroke_width=0.5, stroke_color=FAINT,
                        fill_color=BG, fill_opacity=1.0)
            sq.move_to(np.array([x, y, 0]))
            squares[e["Z"]] = sq
            sym = Text(e["symbol"], font_size=13, color=FAINT, weight=BOLD)
            sym.move_to(sq.get_center())
            symbols[e["Z"]] = sym
            self.add(sq, sym)

        by_cat = {}
        for e in els:
            by_cat.setdefault(e["category"], []).append(e)

        cat_captions = {
            "big_bang": "Big Bang nucleosynthesis (t < 20 min): H, He, trace Li",
            "cosmic_ray_fission": "Cosmic-ray spallation: Li, Be, B",
            "stellar_fusion": "Hydrostatic fusion in stellar cores: C through Al",
            "exploding_massive_stars": "Explosive (silicon) burning, core-collapse supernovae: Si through Ca",
            "exploding_white_dwarfs": "Thermonuclear (Type Ia) supernovae: Fe, Ni -- completes the iron peak",
        }

        prev_sub = None
        for cat in CATEGORY_ORDER_ACT1:
            new_cap = caption(cat_captions[cat], y=-3.55, scale=0.5)
            fade_outs = [FadeOut(prev_sub)] if prev_sub is not None else []
            self.play(*fade_outs, FadeIn(new_cap), run_time=0.4)
            prev_sub = new_cap
            anims = []
            for e in by_cat.get(cat, []):
                sq, sym = squares[e["Z"]], symbols[e["Z"]]
                anims.append(sq.animate.set_fill(colors[e["category"]], opacity=1.0)
                                .set_stroke(BG, width=0.5))
                anims.append(sym.animate.set_color(BG))
            self.play(LaggedStart(*anims, lag_ratio=0.02), run_time=1.3)
            self.wait(0.3)

        self.play(FadeOut(prev_sub), run_time=0.3)

        wall_cap = caption("Fusion has reached the top of the binding-energy curve at iron.", y=-3.55, scale=0.5)
        note = source_note("Element-origin classification: Johnson (2019), Science 363, 474; Burbidge et al. (1957)")
        self.play(FadeIn(wall_cap), FadeIn(note), run_time=0.6)
        self.wait(1.4)
        self.play(FadeOut(wall_cap), FadeOut(note), FadeOut(header), run_time=0.5)
