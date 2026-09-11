# Forged in Starlight
### Nucleosynthetic origin of gold -- a data-driven scientific project in pure Python

This project answers one question with real data and standard physics, and states the answer numerically rather than illustrating it: gold is not made by the fusion that powers stars. It is made by rapid neutron capture (the r-process) in neutron-rich, high-temperature ejecta, and neutron star mergers are one of the observationally confirmed sites where that happens. The analysis is anchored to **GW170817**, the first neutron star merger ever detected (LIGO/Virgo, 2017), using its real, publicly released strain data.

Every quantity that appears in the output -- the chirp mass measured from the merger's real strain data, the r-process path from an iron seed to Au-197, the classification of all 103 elements by formation channel, a sourced timeline for gold's delivery to Earth -- is computed and printed by a physics module before it is plotted or animated. No number is hand-typed into a figure or a video scene.

## What this produces

Running `python main.py` end to end:

1. runs each physics module's own self-check, printing its key numbers to the console;
2. regenerates a set of static matplotlib figures that validate those numbers visually before any further rendering;
3. rebuilds `data/act_data.json`, the single JSON file every rendered section reads its numbers from;
4. renders a five-section results video, `data/forged_in_starlight.mp4`, and concatenates it with ffmpeg.

The video is not a narrative or illustrative film. It is a sequence of labeled, sourced figures -- axes with numeric ticks, data points, fit curves, citations -- in the register of a results presentation, because this is meant to stand as a reproducible scientific submission, not a visualization piece.

## The five sections

| Section | Content | Built from |
|---|---|---|
| **1. Nucleosynthetic origin of the elements** | The periodic table filled in category by category (Big Bang, cosmic-ray spallation, stellar fusion, core-collapse supernovae, Type Ia supernovae), in the order each channel became active. | `physics/origins.py` -- all 103 elements classified by dominant formation process (Johnson 2019; Burbidge et al. 1957) |
| **2. The binding-energy limit** | The binding-energy-per-nucleon curve, plotted from standard published nuclear data, with its peak at Fe-56 marked explicitly and labeled. | Standard published binding-energy values (e.g. Krane, *Introductory Nuclear Physics*) |
| **3. GW170817 and the r-process** | Three data plots in sequence: the real whitened H1 strain around the merger; the chirp mass measured from a sliding-window frequency-ridge fit to that same data, plotted against the analytic post-Newtonian track and compared numerically to the published LIGO/Virgo value; the r-process waiting-point network on a nuclide chart (N vs. Z), landing exactly on Au-197. | `physics/merger.py`, `physics/rprocess.py`, real GW170817 strain data (GWOSC) |
| **4. Delivery of r-process material to Earth** | A timeline of dated events from pre-solar enrichment through core differentiation to the late veneer, each labeled with its age and its published source. | `physics/earth_delivery.py` -- a sourced, order-of-magnitude timeline (Bouvier & Wadhwa 2010; Kleine et al. 2009; Day, Pearson & Taylor 2007) |
| **5. Summary of results** | A results table: measured vs. published chirp mass, the r-process network's final nucleus vs. the gold target, and the element-origin category counts. | All of the above |

## Why this structure

Hydrostatic fusion releases energy while building nuclei up the binding-energy curve toward iron, and *costs* energy past that peak -- so no ordinary stellar fusion process can build anything heavier. Roughly half of the elements past iron are produced by the slow neutron-capture process (s-process) in the outer layers of dying low-mass stars; the rest, including gold, require the rapid process (r-process), which needs a much higher free-neutron density than any quiescent stellar interior provides. Neutron star mergers are one of the sites where the r-process is now understood to run, confirmed observationally when GW170817's electromagnetic counterpart (the kilonova AT2017gfo) showed the spectroscopic signature of freshly synthesized r-process elements. Gold sits at mass number 197, in the tail of the r-process's heaviest abundance peak, produced when neutron-rich progenitor nuclei freeze out of the capture chain and beta-decay down to the first stable isotope at that mass number -- which is gold.

## Repository layout

```
forged_in_starlight/
  main.py                              # orchestrator -- runs the whole pipeline end to end
  requirements.txt
  README.md                            # this file
  DESCRIPTION.md                       # one-paragraph summary
  data/
    gw170817_{H1,L1}_raw_80s.hdf5      # real GW170817 strain, GWOSC, cropped +-40s around merger
    gw170817_{H1,L1}_whitened.hdf5     # whitened + bandpassed (30-400 Hz) versions
    act_data.json                      # precomputed numbers feeding every rendered section (regenerated by scripts/build_act_data.py)
    nuclide_chart.gif                  # correctness-pass: r-process path, N vs Z
    periodic_table_by_origin.png       # correctness-pass: static periodic table by origin
    periodic_table.gif                 # correctness-pass: build-up animation
    earth_timeline.png                 # correctness-pass: Earth gold-delivery timeline
    forged_in_starlight.mp4            # the final rendered video (produced by main.py)
  physics/
    merger.py                          # chirp-mass measurement from real strain data; orbital decay (Peters 1964)
    kilonova.py                        # 3-component Arnett-model light curve (Villar et al. 2017 parameters)
    rprocess.py                        # waiting-point r-process network: iron seed to gold
    origins.py                         # periodic table -> dominant nucleosynthesis channel, all 103 elements
    earth_delivery.py                  # sourced, order-of-magnitude timeline: enrichment -> differentiation -> late veneer
  render/
    nuclide_chart.py                   # correctness-pass matplotlib visual for rprocess.py
    periodic_table.py                  # correctness-pass matplotlib visual for origins.py
    earth_timeline.py                  # correctness-pass matplotlib visual for earth_delivery.py
    cinematic/
      common.py                        # shared visual identity: plain dark background, muted colors, section headers, captions, source notes, axis-numbering helper
      act1_buildup.py .. act5_closing.py   # the five rendered sections described above
  scripts/
    build_act_data.py                  # regenerates data/act_data.json from the physics/ modules
    render_video.py                    # renders all five sections and concatenates them with ffmpeg
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate          # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Manim depends on Cairo, Pango, and a LaTeX distribution (used for numeric axis labels), none of which are pip-installable. If `pip install manim` fails on your platform with a Cairo/Pango build error, or axis numbers fail to render with a `dvisvgm` error:

```bash
# Debian/Ubuntu
sudo apt-get install libcairo2-dev libpango1.0-dev pkg-config python3-dev \
                      texlive-latex-base dvisvgm

# macOS (Homebrew)
brew install cairo pango pkg-config
brew install --cask mactex-no-gui   # or a smaller LaTeX distribution with dvisvgm
```

ffmpeg must also be on `PATH` (used to concatenate the five rendered section videos into one file). See the [Manim installation guide](https://docs.manim.community/en/stable/installation.html) for platform-specific detail.

## Running it

```bash
python main.py                     # everything: physics checks, correctness-pass plots, the full video (720p30)
python main.py --skip-video        # just the physics validation and plots -- fast, no Manim/ffmpeg needed
python main.py --video-quality l   # low-quality (480p15) video, much faster -- good for a first check
python main.py --video-quality h   # high-quality (1080p60) video -- slow
```

Each stage can also be run standalone:

```bash
python -m physics.merger           # prints the measured chirp mass vs. published value
python -m physics.rprocess         # prints the r-process path and confirms it lands on gold
python -m physics.origins          # prints element-origin classification counts
python -m physics.earth_delivery   # prints the Earth gold-delivery timeline
python -m render.nuclide_chart --save     # regenerates data/nuclide_chart.gif
python -m render.periodic_table --save    # regenerates data/periodic_table.gif
python -m render.periodic_table --static  # regenerates data/periodic_table_by_origin.png
python -m render.earth_timeline           # regenerates data/earth_timeline.png
python scripts/build_act_data.py          # regenerates data/act_data.json
python scripts/render_video.py --quality m  # renders and concatenates the five sections directly
```

## What is measured vs. what is illustrative

To be explicit about the evidentiary status of each number, since this is meant to be evaluated as a scientific submission:

- **Measured directly from real data**: the chirp mass in Section 3, computed from a sliding-window frequency-ridge fit to the real, whitened GW170817 H1 strain (`physics/merger.py`). The measured value (1.225 ± 0.500 M☉) is compared numerically, on screen, to the published LIGO/Virgo value (1.188 M☉) rather than simply asserted to match it.
- **Computed from a physical model with standard parameters**: the r-process waiting-point network (`physics/rprocess.py`), which uses standard magic-number shell closures and known half-life systematics to propagate an iron seed nucleus through neutron captures and beta decays; the binding-energy curve (`render/cinematic/act2_wall.py`), plotted from standard published nuclear data.
- **Classification against published criteria**: the element-origin assignment in `physics/origins.py`, following the nucleosynthesis-channel framework in Johnson (2019) and Burbidge et al. (1957).
- **Illustrative but sourced**: the Earth-delivery timeline in `physics/earth_delivery.py`. The relative ordering and approximate ages of each event are drawn from the cited literature, but the timeline is not a dynamical simulation -- it does not model transport, mixing, or accretion physics. This is stated explicitly in the video's Section 4 subtitle.

## Sources

- Abbott, B. P. et al. (LIGO Scientific Collaboration and Virgo Collaboration) (2017). "GW170817: Observation of Gravitational Waves from a Binary Neutron Star Inspiral." *Physical Review Letters* 119, 161101.
- Abbott, B. P. et al. (2017). "Multi-messenger Observations of a Binary Neutron Star Merger." *The Astrophysical Journal Letters* 848, L12.
- GWOSC (Gravitational Wave Open Science Center) -- source of the real H1/L1 strain data used in `data/`.
- Villar, V. A. et al. (2017). "The Combined Ultraviolet, Optical, and Near-Infrared Light Curves of the Kilonova Associated with the Binary Neutron Star Merger GW170817." *The Astrophysical Journal Letters* 851, L21.
- Peters, P. C. (1964). "Gravitational Radiation and the Motion of Two Point Masses." *Physical Review* 136, B1224.
- Arnould, M., Goriely, S., & Takahashi, K. (2007). "The r-process of stellar nucleosynthesis: Astrophysics and nuclear physics achievements and mysteries." *Physics Reports* 450, 97-213.
- Johnson, J. A. (2019). "Populating the periodic table: Nucleosynthesis of the elements." *Science* 363, 474-478.
- Burbidge, E. M., Burbidge, G. R., Fowler, W. A., & Hoyle, F. (1957). "Synthesis of the Elements in Stars." *Reviews of Modern Physics* 29, 547.
- Krane, K. S. *Introductory Nuclear Physics* -- standard binding-energy-per-nucleon reference values.
- Bouvier, A., & Wadhwa, M. (2010). "The age of the Solar System redefined by the oldest Pb-Pb age of a meteoritic inclusion." *Nature Geoscience* 3, 637-641.
- Kleine, T. et al. (2009). "Hf-W chronology of the accretion and early evolution of asteroids and terrestrial planets." *Geochimica et Cosmochimica Acta* 73, 5150-5188.
- Day, J. M. D., Pearson, D. G., & Taylor, L. A. (2007). "Highly Siderophile Element Constraints on Accretion and Differentiation of the Earth-Moon System." *Science* 315, 217-219.

## Reproducibility notes for evaluation

- All physics computations use fixed, documented inputs (real GWOSC strain files bundled in `data/`, standard published constants). Re-running `python main.py` from a clean checkout reproduces the same numbers and the same video content, subject only to floating-point rounding.
- `data/act_data.json` is a build artifact, not a source file -- it is regenerated by `scripts/build_act_data.py` and should not be hand-edited. Deleting it and re-running `python main.py` regenerates it from the physics modules.
- The bundled `data/forged_in_starlight.mp4` is the output of exactly this pipeline; re-rendering should reproduce it up to Manim's own animation-timing determinism (identical figures and numbers, frame-for-frame video output is not guaranteed to be byte-identical across Manim/ffmpeg versions).
