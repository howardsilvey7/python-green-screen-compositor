"""Core chroma-key image compositing functions.

The original project replaced a fixed bright-green RGB value one pixel at a
 time. This module keeps that transparent, educational approach while adding
safe clipping, explicit validation, and reusable functions.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image

RGB = tuple[int, int, int]
DEFAULT_GREEN_KEY: RGB = (0, 231, 26)


@dataclass(frozen=True)
class Placement:
    """One foreground image positioned by its desired center coordinate."""

    foreground: Path
    center_x: int
    center_y: int


def valid_center_bounds(
    background_size: tuple[int, int],
) -> tuple[range, range]:
    """Return valid center coordinates located on the background canvas.

    Foregrounds are allowed to extend beyond the canvas. Pixels that fall
    outside the background are clipped safely during compositing.
    """

    background_width, background_height = background_size

    if background_width <= 0 or background_height <= 0:
        raise ValueError("Background dimensions must be positive.")

    return range(0, background_width), range(0, background_height)


def _validate_center(
    background_size: tuple[int, int],
    center: tuple[int, int],
) -> None:
    """Validate that the requested foreground center lies on the background."""

    x_range, y_range = valid_center_bounds(background_size)
    center_x, center_y = center

    if center_x not in x_range or center_y not in y_range:
        raise ValueError(
            "Foreground center must lie on the background. "
            f"Valid center x: {x_range.start}-{x_range.stop - 1}; "
            f"valid center y: {y_range.start}-{y_range.stop - 1}."
        )


def _paste_non_green_pixels(
    background: Image.Image,
    foreground: Image.Image,
    center: tuple[int, int],
    green_key: RGB,
) -> None:
    """Copy non-key pixels onto the background, clipping at canvas edges."""

    foreground = foreground.convert("RGB")
    foreground_width, foreground_height = foreground.size
    background_width, background_height = background.size
    center_x, center_y = center

    _validate_center(background.size, center)

    offset_x = center_x - foreground_width // 2
    offset_y = center_y - foreground_height // 2

    foreground_pixels = foreground.load()
    background_pixels = background.load()

    for foreground_x in range(foreground_width):
        destination_x = offset_x + foreground_x
        if destination_x < 0 or destination_x >= background_width:
            continue

        for foreground_y in range(foreground_height):
            destination_y = offset_y + foreground_y
            if destination_y < 0 or destination_y >= background_height:
                continue

            colour = foreground_pixels[foreground_x, foreground_y]
            if colour != green_key:
                background_pixels[destination_x, destination_y] = colour


def composite_images(
    background_path: str | Path,
    placements: Iterable[Placement],
    output_path: str | Path,
    *,
    green_key: RGB = DEFAULT_GREEN_KEY,
) -> Path:
    """Composite foregrounds over a background and save the final image."""

    background_path = Path(background_path)
    output_path = Path(output_path)

    if not background_path.is_file():
        raise FileNotFoundError(f"Background image not found: {background_path}")

    with Image.open(background_path) as background_source:
        background = background_source.convert("RGB")

    for placement in placements:
        foreground_path = Path(placement.foreground)
        if not foreground_path.is_file():
            raise FileNotFoundError(f"Foreground image not found: {foreground_path}")

        with Image.open(foreground_path) as foreground:
            _paste_non_green_pixels(
                background,
                foreground,
                (placement.center_x, placement.center_y),
                green_key,
            )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    background.save(output_path)
    return output_path
