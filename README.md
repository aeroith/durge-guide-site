# Durge Guide site

The mod page for Durge Guide, a Baldur's Gate 3 mod. GitHub Pages serves `docs/` from `main`.

- `src/pages/*.html`: the pages. `src/layout.html`, `src/style.css`, `src/print.css`, `src/site.js` and `src/fonts/` are shared.
- `python3 build.py` writes the pages into `docs/` and checks every link and image. `python3 style.py` checks the copy against `STYLE.md`.
- `uv run --with pillow python images.py CAPTURE_DIR` remakes `docs/img/` from the full-size game captures. `uv run --with pillow python images.py --derive` remakes only the crops and WebP sizes.
- `PRODUCT.md` and `DESIGN.md` hold what the site is for and how it looks. `.impeccable/` holds design notes and critiques. None of them are published.

The site works without JavaScript. `src/site.js` only adds to it.

Screenshots are from Baldur's Gate 3, © Larian Studios. This is an unofficial fan project.
