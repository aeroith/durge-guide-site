# Durge Guide site

The mod page for Durge Guide, a Baldur's Gate 3 mod. GitHub Pages serves `docs/` from `main`.

- `src/pages/*.html`: the pages. `src/layout.html` and `src/style.css` are shared.
- `python3 build.py` writes the pages into `docs/` and checks every link and image.
- `uv run --with pillow python images.py CAPTURE_DIR` remakes `docs/img/` from the full-size game captures.

Screenshots are from Baldur's Gate 3, © Larian Studios. This is an unofficial fan project.
