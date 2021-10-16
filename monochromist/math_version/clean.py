from typing import Tuple

import numpy as np
from colour import Color
from PIL import Image, ImageFilter

from .classes import Settings, ImageInfo


#
# def pipeline(img: Image, settings: Settings) -> tuple[Image, Settings]:
#     erased_array, new_settings = erase(img, settings)
#     colored_and_cropped = color_and_crop(erased_array, settings)
#     return colored_and_cropped, new_settings


def erase(img: Image, settings: Settings) -> ImageInfo:
    """Erases pixels and returns numpy array the same shape as image,
     filled with True (save pixel) and False (erase pixel), and settings that were used.
     Parameters will be used if they are defined, otherwise empirical approach will be used."""
    # Convert to grayscale
    converted = img.convert("L")

    # Blur filter is used to average background
    blured = converted.filter(ImageFilter.MedianFilter(settings.thickness))
    values = np.asarray(blured)

    if settings.saving:
        threshold = user_percentile(values, settings)
    else:
        threshold = empirical_percentile(values)

    erased = values < threshold

    return ImageInfo(img, settings, erased)


def user_percentile(arr: np.array, settings: Settings) -> int:
    return np.percentile(arr.flatten(), settings.saving, axis=0)


def empirical_percentile(arr: np.array) -> int:
    percentiles = [np.percentile(arr.flatten(), i, axis=0) for i in range(101)]
    # y = K * x + b
    K = 1.0
    b_values = np.array([y - K * x for (x, y) in enumerate(percentiles)])

    return np.argmax(b_values)[0]

#
# def color_and_crop(arr: np.array, settings: Settings) -> Image:
#     """Color non-transparent pixels with selected color"""
#
#     color_tuple = color2tuple(settings.color)
#     transparent = [0, 0, 0, 0]
#
#     def color_row(row: np.array) -> np.array:
#         return np.array([color_tuple if x else transparent for x in row])
#
#     colored = np.apply_along_axis(color_row, 1, arr)
#     new_image = Image.fromarray(np.uint8(colored), "RGBA")
#
#     if settings.crop and arr.any():
#         borders = find_borders(arr)
#         cropped_image = new_image.crop(borders)
#
#     return cropped_image


# def crop(img: Image, settings: Settings) -> Image:
#     as_array = np.asarray(img)
#     if settings.crop and as_array.any():
#         borders = find_borders(as_array)
#         cropped_image = img.crop(borders)
#     else:
#         cropped_image = img
#     return cropped_image

#
# def clean_image(img: Image, settings: Settings) -> Image:
#     """Clean background and color contour to selected color"""
#
#
#
#     perts = [np.percentile(values.flatten(), i, axis=0) for i in range(101)]
#     # print([(values < p).sum() for p in perts])
#     print(perts)
#
#     # threshold = find_threshold(values, settings)
#     threshold = np.percentile(values.flatten(), settings.saving, axis=0)
#     cleaned_array = values <= threshold
#     colored_image = color_image(img, cleaned_array, settings)
#
#     # TODO: remove artifacts with alone pixels
#
#     if settings.crop and cleaned_array.any():
#         borders = find_borders(cleaned_array)
#         colored_image = colored_image.crop(borders)
#
#     return colored_image

#
# def find_threshold(arr: np.ndarray, settings: Settings) -> float:
#     """Find threshold using percentiles.
#     Main idea: pixels from contour happens very rarely and should be near 0-th percentile"""
#
#     flattened = arr.flatten()
#     step_for_percentiles = 10
#
#     percentiles = [np.percentile(flattened, i, axis=0) for i in range(0, 101, step_for_percentiles)]
#     return (1 - settings.saving) * percentiles[0] + settings.saving * percentiles[-1]

#
# def color_image(img: Image, arr: np.array, settings: Settings) -> Image:
#     """Color non-transparent pixels with selected color"""
#
#     color_tuple = color2tuple(settings.color)
#     transparent = [0, 0, 0, 0]
#
#     def color_row(row: np.array) -> np.array:
#         return np.array([color_tuple if x else transparent for x in row])
#
#     colored = np.apply_along_axis(color_row, 1, arr)
#     new_image = Image.fromarray(np.uint8(colored), "RGBA")
#     return new_image


# def find_borders(arr: np.array) -> Tuple[int, int, int, int]:
#     """Find transparent borders"""
#
#     notna_columns = arr.any(axis=0)
#     notna_rows = arr.any(axis=1)
#
#     left = np.flatnonzero(notna_columns)[0]
#     right = np.flatnonzero(notna_columns)[-1]
#
#     upper = np.flatnonzero(notna_rows)[0]
#     lower = np.flatnonzero(notna_rows)[-1]
#
#     return left, upper, right, lower
#
#
# def color2tuple(color: Color) -> [int]:
#     """Convert color to RGBA tuple"""
#     r, g, b = [int(255 * x) for x in color.rgb]
#     alpha_channel = 255
#     return [r, g, b, alpha_channel]
