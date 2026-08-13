"""Command-line interface for the green-screen compositor."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from .compositor import Placement, composite_images, valid_center_bounds

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BACKGROUNDS_DIR = PROJECT_ROOT / "assets" / "backgrounds"
DEFAULT_FOREGROUNDS_DIR = PROJECT_ROOT / "assets" / "foregrounds"
DEFAULT_OUTPUT = PROJECT_ROOT / "outputs" / "output.bmp"


def _integer_between(prompt: str, minimum: int, maximum: int) -> int:
    """Prompt until the user enters an integer within the requested bounds."""

    while True:
        raw_value = input(prompt).strip()
        try:
            value = int(raw_value)
        except ValueError:
            print("Please enter a whole number.")
            continue

        if minimum <= value <= maximum:
            return value

        print(f"Please enter a value from {minimum} to {maximum}.")


def _choose_image(image_paths: list[Path], heading: str, prompt: str) -> Path:
    """Display numbered image choices and return the selected path."""

    print(f"\n{heading}:")
    for index, path in enumerate(image_paths, start=1):
        print(f"  {index}. {path.name}")

    selection = _integer_between(prompt, 1, len(image_paths))
    return image_paths[selection - 1]


def _choose_background(backgrounds_dir: Path) -> Path:
    available = sorted(backgrounds_dir.glob("*.bmp"))
    if not available:
        raise FileNotFoundError(f"No background files found in {backgrounds_dir}")

    return _choose_image(
        available,
        "Available backgrounds",
        "Choose a background number: ",
    )


def _collect_placements(
    background_path: Path,
    foregrounds_dir: Path,
) -> list[Placement]:
    foregrounds = sorted(foregrounds_dir.glob("ninja_image_*.bmp"))
    if not foregrounds:
        raise FileNotFoundError(f"No foreground files found in {foregrounds_dir}")

    count = _integer_between(
        f"How many foreground images would you like (1-{len(foregrounds)})? ",
        1,
        len(foregrounds),
    )

    with Image.open(background_path) as background:
        background_size = background.size

    x_range, y_range = valid_center_bounds(background_size)
    placements: list[Placement] = []

    for placement_number in range(1, count + 1):
        foreground_path = _choose_image(
            foregrounds,
            f"Available foregrounds for placement {placement_number}",
            "Choose a foreground number: ",
        )

        with Image.open(foreground_path) as foreground:
            foreground_size = foreground.size

        print(
            f"Selected {foreground_path.name} ({foreground_size[0]}x{foreground_size[1]})."
        )
        print(
            "Choose its center on the background. If part of the foreground "
            "extends beyond an edge, that portion will be clipped safely."
        )

        center_x = _integer_between(
            f"  x ({x_range.start}-{x_range.stop - 1}): ",
            x_range.start,
            x_range.stop - 1,
        )
        center_y = _integer_between(
            f"  y ({y_range.start}-{y_range.stop - 1}): ",
            y_range.start,
            y_range.stop - 1,
        )

        placements.append(Placement(foreground_path, center_x, center_y))

    return placements


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Composite supplied foreground bitmaps over a background by "
            "removing a fixed green key."
        )
    )
    parser.add_argument(
        "--background",
        type=Path,
        help="Background image path. If omitted, interactive selection is used.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output image path (default: {DEFAULT_OUTPUT}).",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    background_path = args.background or _choose_background(DEFAULT_BACKGROUNDS_DIR)

    if not background_path.is_absolute():
        background_path = PROJECT_ROOT / background_path

    placements = _collect_placements(background_path, DEFAULT_FOREGROUNDS_DIR)
    saved_path = composite_images(background_path, placements, args.output)

    print(f"\nDone. Composite image saved to: {saved_path}")


if __name__ == "__main__":
    main()
