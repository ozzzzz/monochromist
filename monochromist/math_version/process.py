import os
from pathlib import Path

import click
from colour import Color
from loguru import logger
from PIL import Image

from monochromist.math_version.clean import erase
from monochromist.math_version.postprocess import color_and_crop
from .classes import Settings


@click.command()
@click.option("-i", "--input", type=Path, required=True, help="Input filepath")
@click.option("-o", "--output", type=Path, required=True, help="Output filepath")
@click.option(
    "-t",
    "--thickness",
    type=int,
    help="Thickness of the line",
    default=3,
    show_default=True,
)
@click.option(
    "-s",
    "--saving",
    type=int,
    help="From 0 to 1: the closer to one, the more pixels will be left",
    default=3,
    show_default=True,
)
@click.option(
    "-c",
    "--color",
    type=str,
    help="Color of result contour",
    default="black",
    show_default=True,
)
@click.option(
    "-p",
    "--crop",
    type=bool,
    help="Crop transparent pixels after converting",
    default=True,
    show_default=True,
)
def process(
    input: Path, output: Path, thickness: int, saving: int, color: Color, crop: bool
) -> None:
    """Take contour from selected file"""
    process_file(input, output, thickness, saving, color, crop)


def process_file(
    input: Path,
    output: Path,
    thickness: int = 3,
    saving: int = 3,
    color: Color = "black",
    crop: bool = True,
) -> None:
    """Take contour from selected file"""
    parsed_color = Color(color)

    settings = Settings(
        thickness=thickness,
        saving=saving,
        color=parsed_color,
        crop=crop,
    )

    initial_image = Image.open(input)
    image_info = erase(initial_image, settings)
    new_image = color_and_crop(image_info)

    if os.path.exists(output):
        os.remove(output)
    new_image.save(output)

    logger.info(f"{input} --> {output}")
    logger.info(image_info.settings)


if __name__ == "__main__":
    process()
