"""Green-screen bitmap compositing package."""

from .compositor import DEFAULT_GREEN_KEY, Placement, composite_images, valid_center_bounds

__all__ = [
    "DEFAULT_GREEN_KEY",
    "Placement",
    "composite_images",
    "valid_center_bounds",
]
