"""
Forged in Starlight -- orchestrator.

Runs the whole pipeline end to end, in order:

  1. Physics validation  -- runs every physics/*.py module's own self-check
                             (each prints its key numbers: measured chirp
                             mass vs. published, kilonova peak luminosity,
                             the r-process path landing on gold, the
                             element-origin counts, the Earth-delivery
                             timeline).
  2. Correctness-pass visuals -- regenerates the plain matplotlib figures
                             in data/ (nuclide chart, periodic table by
                             origin, Earth timeline) that validate each
                             physics module's output before any cinematic
                             styling is applied.
  3. Results-video data    -- rebuilds data/act_data.json, the single
                             source of numbers every rendered section reads.
  4. Results video          -- renders all five sections (Manim) and
                             concatenates them into data/forged_in_starlight.mp4.

Each stage can be skipped with a flag, since step 4 (video rendering) is by
far the slowest part and a reviewer may want the physics/plots without
waiting for a full render.

Usage (from this directory):
    python main.py                    # everything, medium-quality video
    python main.py --skip-video       # physics + plots only, no video
    python main.py --video-quality l  # fast low-quality video preview
    python main.py --video-quality h  # high-quality 1080p60 video

Requires: pip install -r requirements.txt, and ffmpeg on PATH for the
video-concatenation step. See README.md for full setup and an explanation
of what each stage validates.
"""

import argparse
import runpy
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PHYSICS_MODULES = [
    "physics.merger",
    "physics.kilonova",
    "physics.rprocess",
    "physics.origins",
    "physics.earth_delivery",
]

CORRECTNESS_VISUALS = [
    ("render.nuclide_chart", ["--save"]),
    ("render.periodic_table", ["--static"]),
    ("render.periodic_table", ["--save"]),
    ("render.earth_timeline", []),
]


def run_module(module, args=None):
    cmd = [sys.executable, "-m", module] + (args or [])
    print(f"\n$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        print(f"FAILED: {module} exited with {result.returncode}")
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                       formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--skip-physics", action="store_true", help="skip physics validation prints")
    parser.add_argument("--skip-visuals", action="store_true", help="skip correctness-pass matplotlib figures")
    parser.add_argument("--skip-video", action="store_true", help="skip the Manim cinematic render entirely")
    parser.add_argument("--video-quality", choices=["l", "m", "h"], default="m",
                         help="l=fast preview, m=720p30 (default), h=1080p60")
    args = parser.parse_args()

    if not args.skip_physics:
        print("=" * 70)
        print("STAGE 1: physics validation")
        print("=" * 70)
        for mod in PHYSICS_MODULES:
            run_module(mod)

    if not args.skip_visuals:
        print("\n" + "=" * 70)
        print("STAGE 2: correctness-pass visuals (data/*.png, *.gif)")
        print("=" * 70)
        for mod, mod_args in CORRECTNESS_VISUALS:
            run_module(mod, mod_args)

    print("\n" + "=" * 70)
    print("STAGE 3: rebuilding data/act_data.json for the results video")
    print("=" * 70)
    run_module("scripts.build_act_data")

    if not args.skip_video:
        print("\n" + "=" * 70)
        print("STAGE 4: rendering the results video (this is the slow part)")
        print("=" * 70)
        run_module("scripts.render_video", ["--quality", args.video_quality])
        print("\nDone. Final video: data/forged_in_starlight.mp4")
    else:
        print("\nSkipped video rendering (--skip-video). Physics results and "
               "correctness-pass figures are in data/.")


if __name__ == "__main__":
    main()
