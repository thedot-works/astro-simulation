"""Shared visual identity and data loading for the results-video pass
(build plan Phase 4). This is deliberately plain: publication-style dark
background, one accent color for gold, monospace-adjacent sans type, and
nothing decorative. No starfields, no transition effects, no illustrative
iconography -- every visual element here maps to a labeled, sourced
quantity. Every act imports from here so that restraint is consistent
throughout.
"""

import json
from pathlib import Path

from manim import *

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "act_data.json"

BG = "#0a0a0c"
GOLD = "#c9a227"       # a muted, print-safe gold -- not a glowing/neon tone
INK = "#e8e8ea"
DIM = "#9096a0"
FAINT = "#33363d"
CAPTURE_COLOR = "#4a90a4"   # neutron capture -- muted teal
DECAY_COLOR = "#b5651d"     # beta decay -- muted rust

config.background_color = BG


def load_data():
    with open(DATA_PATH) as f:
        return json.load(f)


def section_title(number, title, subtitle=None):
    """A plain section header: 'Section N -- Title', used at the top of
    every scene rather than a title card. Stays on screen for the whole
    scene in most acts (added by the caller), consistent with how a
    labeled figure keeps its title.
    """
    group = VGroup()
    t = Text(f"{number}. {title}", font_size=30, color=INK, weight=BOLD)
    group.add(t)
    if subtitle:
        s = Text(subtitle, font_size=20, color=DIM)
        s.next_to(t, DOWN, buff=0.15)
        group.add(s)
    group.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    group.to_corner(UL, buff=0.4)
    return group


def caption(text, y=-3.4, scale=0.55, color=INK):
    """A bottom-of-frame caption -- plain, factual, no emphasis styling
    beyond what a figure caption would carry."""
    t = Text(text, font_size=30, color=color).scale(scale)
    t.move_to(np.array([0, y, 0]))
    return t


def subcaption(text, y=-4.05, scale=0.4, color=DIM):
    t = Text(text, font_size=24, color=color).scale(scale)
    t.move_to(np.array([0, y, 0]))
    return t


def source_note(text, y=-4.55):
    """A small citation line, bottom-right, the way a figure credits its
    data source. Present on every scene that shows measured or sourced
    data."""
    t = Text(text, font_size=16, color=FAINT, slant=ITALIC)
    t.to_edge(DOWN, buff=0.15).to_edge(RIGHT, buff=0.4)
    return t


def add_axis_numbers(axes, font_size=16, num_decimal_places=0, color=DIM):
    """Adds plain numeric tick labels to both axes of a Manim Axes object.
    A figure axis with unlabeled ticks is not publication-quality -- every
    Axes used in this pipeline should call this immediately after creation.
    """
    axes.x_axis.add_numbers(font_size=font_size, num_decimal_places=num_decimal_places, color=color)
    axes.y_axis.add_numbers(font_size=font_size, num_decimal_places=num_decimal_places, color=color)
    return axes
