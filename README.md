# Closet Compass

A free, source-checked directory of places in Tennessee to borrow or donate medical equipment: wheelchairs, walkers, shower chairs, hospital beds and more.

The site is static HTML built by `build.py` into `docs/`, which GitHub Pages serves. Yeha, an AI research agent, adds or re-verifies one useful page each night. Its operating manual is `yeha/YEHA.md`.

## Build locally

```bash
pip install -r requirements.txt
python3 build.py --base-path "" --site-url http://localhost:8000
python3 tools/check.py
python3 -m http.server 8000 -d docs
```

## Edit

- Listings: `data/listings.json` (every fact needs a source and a `last_checked` date)
- Guides and pages: `content/**/*.md`
- Settings: `config.json` (site URL, base path, Amazon tag, deck link, form URL)
