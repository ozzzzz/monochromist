from typing import Tuple

import numpy as np
from colour import Color
from PIL import Image, ImageFilter

from .classes import Settings


def clean_image(img: Image, settings: Settings) -> Image:
    """Clean background and color contour to selected color"""

    # Convert to grayscale and blur picture.
    converted = img.convert("L")

    # Blur filter is used to average background
    blured = converted.filter(ImageFilter.MedianFilter(settings.thickness))
    values = np.asarray(blured)

    threshold = find_threshold(values, settings)
    cleaned_array = values < threshold
    colored_image = color_image(img, cleaned_array, settings)

    # TODO: remove artifacts with alone pixels

    if settings.crop and cleaned_array.any():
        borders = find_borders(cleaned_array)
        colored_image = colored_image.crop(borders)

    return colored_image


def find_threshold(arr: np.ndarray, settings: Settings) -> float:
    """Find threshold using percentiles.
    Main idea: pixels from contour happens very rarely and should be near 0-th percentile"""

    flattened = arr.flatten()
    step_for_percentiles = 10
    percentiles = [np.percentile(flattened, i, axis=0) for i in range(0, 101, step_for_percentiles)]
    return (1 - settings.alpha) * percentiles[0] + settings.alpha * np.mean(percentiles[1:])


def color_image(img: Image, arr: np.array, settings: Settings) -> Image:
    """Color non-transparent pixels with selected color"""

    color_tuple = color2tuple(settings.color)
    transparent = (0, 0, 0, 0)

    colored = [color_tuple if x else transparent for x in arr.flatten()]
    new_image = img.convert("RGBA")
    new_image.putdata(colored)
    return new_image


def find_borders(arr: np.array) -> Tuple[int, int, int, int]:
    """Find transparent borders"""

    notna_columns = arr.any(axis=0)
    notna_rows = arr.any(axis=1)

    left = np.flatnonzero(notna_columns)[0]
    right = np.flatnonzero(notna_columns)[-1]

    upper = np.flatnonzero(notna_rows)[0]
    lower = np.flatnonzero(notna_rows)[-1]

    return left, upper, right, lower


def color2tuple(color: Color) -> Tuple[int, int, int, int]:
    """Convert color to RGBA tuple"""
    r, g, b = [int(255 * x) for x in color.rgb]
    alpha_channel = 255
    return r, g, b, alpha_channel
