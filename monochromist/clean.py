import numpy as np
from PIL import Image, ImageFilter

from .classes import Settings


def clean_image(img: Image, settings: Settings) -> Image:
    """Clean background and color contour to selected color"""

    # convert to grayscale
    converted = img.convert("LA")

    # find threshold (use thickness as a parameter to blur filter)
    blured = converted.filter(ImageFilter.MedianFilter(settings.thickness))

    # Main idea: contrast pixels are happens rarely, other pixels are background.
    # Thus we make something like histogram using percentiles and take only pixels near zero percentile.
    values = list(np.asarray(blured)[..., 0].ravel())
    step_for_percentiles = 10
    percentiles = [
        np.percentile(values, i, axis=0) for i in range(0, 101, step_for_percentiles)
    ]
    threshold = settings.alpha * percentiles[0] + (1 - settings.alpha) * np.mean(
        percentiles[1:]
    )

    # clean image
    # TODO: refactor with image size
    old_image_data = converted.getdata()
    new_image = converted.copy()
    new_image_data = []

    for index in range(len(old_image_data)):
        if values[index] > threshold:
            # make transparent
            new_image_data.append((255, 0))
        else:
            # fill with the color
            # TODO: replace with color
            new_image_data.append((255, 255))

    new_image.putdata(new_image_data)

    # TODO: add crop feature

    return new_image
