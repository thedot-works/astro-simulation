"""
Renders every act of the cinematic video and concatenates them into one
file: data/forged_in_starlight.mp4.

Requires Manim and ffmpeg to be installed (see README.md / requirements.txt).
Run from the forged_in_starlight/ directory:

    python scripts/render_video.py            # medium quality (720p30)
    python scripts/render_video.py --quality l # low quality, fast preview
    python scripts/render_video.py --quality h # high quality (1080p60)
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ACTS = [
    ("render/cinematic/act1_buildup.py", "Act1Buildup"),
    ("render/cinematic/act2_wall.py", "Act2Wall"),
    ("render/cinematic/act3_rprocess.py", "Act3RProcess"),
    ("render/cinematic/act4_earth.py", "Act4Earth"),
    ("render/cinematic/act5_closing.py", "Act5Closing"),
]

QUALITY_FLAG = {"l": "-ql", "m": "-qm", "h": "-qh"}
QUALITY_DIR = {"l": "480p15", "m": "720p30", "h": "1080p60"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quality", choices=["l", "m", "h"], default="m")
    args = parser.parse_args()

    flag = QUALITY_FLAG[args.quality]
    qdir = QUALITY_DIR[args.quality]

    for script, scene in ACTS:
        print(f"=== rendering {scene} ({qdir}) ===")
        result = subprocess.run(
            [sys.executable, "-m", "manim", flag, script, scene],
            cwd=ROOT,
        )
        if result.returncode != 0:
            print(f"FAILED rendering {scene} -- aborting.")
            sys.exit(result.returncode)

    concat_path = ROOT / "data" / "concat_list.txt"
    with open(concat_path, "w") as f:
        for script, scene in ACTS:
            module_name = Path(script).stem
            video_path = ROOT / "media" / "videos" / module_name / qdir / f"{scene}.mp4"
            f.write(f"file '{video_path}'\n")

    out_path = ROOT / "data" / "forged_in_starlight.mp4"
    print(f"=== concatenating into {out_path} ===")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_path),
         "-c", "copy", str(out_path)],
        check=True,
    )
    print(f"Done: {out_path}")


if __name__ == "__main__":
    main()
