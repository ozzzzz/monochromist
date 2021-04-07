from pathlib import Path
from typing import NamedTuple

from colour import Color


class Settings(NamedTuple):
    """Tools settings"""

    in_file: Path
    """Input file"""

    out_file: Path
    """Output file"""

    thickness: int
    """Thickness of the line, used in algorithm to set blur radius"""

    alpha: float
    """Threshold for background from zero to one.
    The closer to one, the more pixels will be left"""

    color: Color
    """Final color of contour"""

    crop: bool
    """Crop transparent pixels after converting"""
