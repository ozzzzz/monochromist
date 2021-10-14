import os
from pathlib import Path

import click
from colour import Color
from loguru import logger
from PIL import Image

from .classes import Settings
from .clean import clean_image


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
    "-a",
    "--alpha",
    type=float,
    help="From 0 to 1: the closer to one, the more pixels will be left",
    default=0.3,
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
    input: Path, output: Path, thickness: int, alpha: float, color: Color, crop: bool
) -> None:
    """Take contour from selected file"""
    process_file(input, output, thickness, alpha, color, crop)


def process_file(
    input: Path,
    output: Path,
    thickness: int = 3,
    alpha: float = 0.3,
    color: Color = "black",
    crop: bool = True,
) -> None:
    """Take contour from selected file"""
    parsed_color = Color(color)

    settings = Settings(
        in_file=input,
        out_file=output,
        thickness=thickness,
        alpha=alpha,
        color=parsed_color,
        crop=crop,
    )

    initial_image = Image.open(input)
    result_image = clean_image(initial_image, settings)
    if os.path.exists(output):
        os.remove(output)
    result_image.save(output)

    logger.info(f"{input} --> {output}")


if __name__ == "__main__":
    process()
