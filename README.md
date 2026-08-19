# Python Green-Screen Bitmap Compositor

![Tests](https://github.com/howardsilvey7/python-green-screen-compositor/actions/workflows/tests.yml/badge.svg)

A compact Python image-processing project that removes a fixed green-screen colour from supplied foreground bitmaps and composites the remaining pixels over a selected background.

**Author:** Howard R. Silvey

The project was originally built as an interactive bitmap-programming exercise and later refactored into a reusable, testable, headless Python package suitable for reproducible execution from a local development environment.

## What the project demonstrates

- direct pixel-level RGB processing;
- chroma-key / green-screen compositing;
- image coordinate systems and centered placement;
- safe edge clipping and coordinate validation;
- reusable Python functions and dataclasses;
- command-line input validation;
- deterministic project structure and generated outputs;
- automated tests for core compositing behaviour.

## Repository structure

```text
python-green-screen-compositor/
├── README.md
├── RUNNING.md
├── LICENSE
├── .gitignore
├── pyproject.toml
├── assets/
│   ├── backgrounds/
│   └── foregrounds/
├── outputs/
│   ├── README.md
│   └── example-output.bmp
├── src/
│   └── green_screen/
│       ├── __init__.py
│       ├── __main__.py
│       ├── compositor.py
│       └── cli.py
└── tests/
    └── test_compositor.py
```

## Core algorithm

The original exercise used an exact bright-green key:

```text
RGB(0, 231, 26)
```

For each foreground pixel, the compositor checks its RGB value. Pixels matching the key are treated as transparent; every other pixel is copied onto the background at the corresponding centered destination coordinate.

The refactor preserves that explicit pixel-level algorithm rather than replacing it with a black-box chroma-key library operation.

## Improvements in the refactored version

The refactor:

- removes Replit-specific configuration and temporary files;
- removes the graphical display requirement so the project runs headlessly;
- replaces duplicate program implementations with one authoritative package;
- safely clips foreground pixels that extend beyond a background edge instead of crashing;
- validates that requested foreground centers lie on the selected background;
- lets the user choose each foreground image rather than forcing numbered order;
- handles invalid numeric input interactively;
- uses descriptive names and structured functions;
- separates core compositing logic from CLI interaction;
- modernizes packaging and dependency metadata;
- adds automated tests;
- organizes image assets and generated output into dedicated directories.

## Quick start

See [RUNNING.md](RUNNING.md) for complete setup and execution instructions.

After installation, run interactively with:

```bash
python -m green_screen
```

or, after package installation:

```bash
green-screen
```

## Generated output policy

A representative generated image is committed under `outputs/` so repository viewers can inspect a result immediately.

Running the compositor may regenerate or overwrite output files. This intentionally combines portfolio visibility with reproducibility from source.

## License

See [LICENSE](LICENSE).
