# Forged in Starlight — 3D cinematic cut

A second visual treatment of the same project, prioritizing cinematic 3D
spectacle over the plain-plot register in `forged_in_starlight/`. Same
underlying physics and real GW170817 data (read from
`forged_in_starlight/data/act_data.json`), rendered as one continuous film
with no on-screen section headers.

**Final video:** `../data/forged_in_starlight_3d.mp4` (20s, 1280x720).

**Interactive companion:** "Forge a Metal" — `metal_explorer.html` is the
source for a published interactive tool (ported from `physics/rprocess.py`
and `physics/origins.py` to JS) that lets you dial in r-process conditions
and see which real element results. Open the file directly in a browser,
or view the published version at:
https://claude.ai/code/artifact/754fdd12-6684-4812-8c4c-e044b1b139fa

## How the film is built

Three.js scene (`scenes/story.html`) + Playwright/Chromium headless
screenshot capture, one deterministic frame at a time (no reliance on
real-time animation — `window.__renderFrame(i, total)` is called explicitly
per frame), then ffmpeg encodes the PNG sequence to video.

```
npm install three playwright
```

Three.js's ES module build needs real HTTP (not `file://`) because of CORS
on module imports, so serve the `scenes/` folder locally first:

```
cd scenes
python3 -m http.server 8931 --bind 127.0.0.1
```

Then, from `cinematic_3d/`, capture frames and encode:

```
node capture.js scenes/story.html frames/story 480
ffmpeg -framerate 24 -i frames/story/frame_%05d.png -c:v libx264 -pix_fmt yuv420p -crf 20 out.mp4
```

`scenes/merger.html` is the standalone neutron-star-merger scene from an
earlier iteration of the same pipeline (kept for reference); `story.html`
is the full five-beat film and the current source of truth.

Note: `three.module.js`, `three.core.js`, and the `addons/postprocessing`
and `addons/shaders` files that `scenes/story.html` imports are the
unmodified Three.js library and its EffectComposer/UnrealBloomPass
dependencies (from the `three` npm package's `build/` and
`examples/jsm/` folders) — not committed here to keep the repo small.
After `npm install three`, copy them into `scenes/` and `scenes/addons/`
matching the import paths in `story.html`, or adjust the import map to
point at `node_modules/three` directly.
