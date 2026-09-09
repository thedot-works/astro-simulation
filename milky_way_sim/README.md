# Milky Way & Sagittarius A* — Python simulation

Pure Python (numpy, matplotlib, pandas) — no notebook, no HTML/JS.

## Files

- `constants.py` — physical constants and the Galaxy's rotation-curve model
- `solar_system.py` — the eight planets on Keplerian orbits, with a Kepler's-Third-Law check against observed periods
- `galaxy.py` — the Milky Way's spiral structure, rotating differentially about Sagittarius A*
- `main.py` — runs both

## Setup

```
pip install -r requirements.txt
```

## Run

```
python main.py            # opens both animations as interactive windows
python main.py --save     # writes solar_system.gif and milky_way.gif instead

python solar_system.py    # just the solar system
python galaxy.py          # just the galaxy
python constants.py       # prints the derived galactic year and mass check
```

## Physics notes

- Kepler's Third Law (`T[yr] = a[AU]^1.5`) reproduces every planet's observed
  period to well under 1%.
- The galaxy's rotation uses the Milky Way's actual measured flat rotation
  curve (~220 km/s beyond ~3 kpc), so the field rotates *differentially* —
  inner stars complete an orbit faster than outer ones — rather than
  spinning as a rigid disk. The Sun's derived galactic year comes out to
  ~228 Myr, matching the commonly cited 220–230 Myr range.
- Sgr A*'s ~4.3 million solar masses are a small fraction of the ~10¹¹
  solar masses enclosed within the solar orbit — the Sun's orbital speed is
  set mostly by the disk, bulge, and dark-matter halo, not the black hole.

## References

- GRAVITY Collaboration, Abuter, R. et al. (2022). *A&A*, 657, L12. (Sgr A* mass)
- GRAVITY Collaboration (2019). *A&A*, 625, L10. (Sun–Sgr A* distance)
- Reid, M. J. & Honma, M. (2014). *ARA&A*, 52, 339–372. (rotation curve)
- Vallée, J. P. (2017). *ApJ*, 835, 128. (spiral pitch angle)
- Williams, D. R. *NASA Planetary Fact Sheets*, nssdc.gsfc.nasa.gov/planetary/factsheet/
