from pathlib import Path

import pytest
from PIL import Image

from green_screen.compositor import Placement, composite_images, valid_center_bounds


def test_valid_center_bounds_cover_background_canvas() -> None:
    x_range, y_range = valid_center_bounds((100, 80))

    assert (x_range.start, x_range.stop - 1) == (0, 99)
    assert (y_range.start, y_range.stop - 1) == (0, 79)


def test_exact_green_pixels_are_transparent(tmp_path: Path) -> None:
    background_path = tmp_path / "background.bmp"
    foreground_path = tmp_path / "foreground.bmp"
    output_path = tmp_path / "output.bmp"

    Image.new("RGB", (5, 5), (10, 20, 30)).save(background_path)

    foreground = Image.new("RGB", (3, 3), (0, 231, 26))
    foreground.putpixel((1, 1), (200, 100, 50))
    foreground.save(foreground_path)

    composite_images(
        background_path,
        [Placement(foreground_path, 2, 2)],
        output_path,
    )

    output = Image.open(output_path).convert("RGB")
    assert output.getpixel((2, 2)) == (200, 100, 50)
    assert output.getpixel((1, 1)) == (10, 20, 30)


def test_foreground_is_clipped_safely_at_background_edge(tmp_path: Path) -> None:
    background_path = tmp_path / "background.bmp"
    foreground_path = tmp_path / "foreground.bmp"
    output_path = tmp_path / "output.bmp"

    Image.new("RGB", (4, 4), (0, 0, 0)).save(background_path)
    Image.new("RGB", (6, 6), (255, 0, 0)).save(foreground_path)

    composite_images(
        background_path,
        [Placement(foreground_path, 0, 0)],
        output_path,
    )

    output = Image.open(output_path).convert("RGB")
    assert output.size == (4, 4)
    assert output.getpixel((0, 0)) == (255, 0, 0)
    assert output.getpixel((3, 3)) == (0, 0, 0)


def test_foreground_larger_than_background_is_supported(tmp_path: Path) -> None:
    background_path = tmp_path / "background.bmp"
    foreground_path = tmp_path / "foreground.bmp"
    output_path = tmp_path / "output.bmp"

    Image.new("RGB", (5, 3), (10, 20, 30)).save(background_path)
    Image.new("RGB", (7, 7), (100, 110, 120)).save(foreground_path)

    composite_images(
        background_path,
        [Placement(foreground_path, 2, 1)],
        output_path,
    )

    output = Image.open(output_path).convert("RGB")
    assert output.size == (5, 3)
    assert output.getpixel((0, 0)) == (100, 110, 120)
    assert output.getpixel((4, 2)) == (100, 110, 120)


def test_center_outside_background_is_rejected(tmp_path: Path) -> None:
    background_path = tmp_path / "background.bmp"
    foreground_path = tmp_path / "foreground.bmp"

    Image.new("RGB", (10, 10), (0, 0, 0)).save(background_path)
    Image.new("RGB", (3, 3), (255, 0, 0)).save(foreground_path)

    with pytest.raises(ValueError, match="center must lie on the background"):
        composite_images(
            background_path,
            [Placement(foreground_path, 10, 5)],
            tmp_path / "output.bmp",
        )
