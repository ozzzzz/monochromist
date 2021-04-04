from typing import Tuple

import numpy as np
from colour import Color
from PIL import Image, ImageFilter

from .classes import Settings


def clean_image(img: Image, settings: Settings) -> Image:
    """Clean background and color contour to selected color"""

    # Convert to grayscale.
    converted = img.convert("LA")

    # Find threshold (use thickness as a parameter to blur filter).
    # Main idea: contrast pixels are happens rarely, other pixels are background.
    # Thus we make something like histogram using percentiles and take only pixels near zero percentile.
    blured = converted.filter(ImageFilter.MedianFilter(settings.thickness))
    values = list(np.asarray(blured)[..., 0].ravel())
    step_for_percentiles = 10
    percentiles = [np.percentile(values, i, axis=0) for i in range(0, 101, step_for_percentiles)]
    threshold = settings.alpha * percentiles[0] + (1 - settings.alpha) * np.mean(percentiles[1:])

    # Clean image.
    color_tuple = color2tuple(settings.color)
    transparent = (0, 0, 0, 0)

    def threshold_func(index: int) -> Tuple[int, int, int, int]:
        if values[index] > threshold:
            return transparent
        else:
            return color_tuple

    width, height = img.size
    new_image = img.convert("RGBA")
    new_image_data = [threshold_func(index) for index in range(width * height)]
    new_image.putdata(new_image_data)

    # TODO: add crop feature

    return new_image


def color2tuple(color: Color) -> Tuple[int, int, int, int]:
    """Convert color to RGBA tuple"""
    r, g, b = [int(255 * x) for x in color.rgb]
    alpha_channel = 255
    return r, g, b, alpha_channel
