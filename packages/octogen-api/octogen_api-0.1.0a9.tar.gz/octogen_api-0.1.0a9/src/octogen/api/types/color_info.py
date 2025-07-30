# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["ColorInfo", "Color"]


class Color(BaseModel):
    label: str
    """The color display name, or label.

    This may differ from standard color family names.
    """

    hex_code: Optional[str] = None
    """The hex code of the color."""

    swatch_url: Optional[str] = None
    """A URL pointing to the color swatch image."""


class ColorInfo(BaseModel):
    color_families: Optional[List[str]] = None
    """Standard color families, such as 'Red', 'Green', 'Blue'. Maximum 5 values."""

    colors: Optional[List[Color]] = None
    """Color display names, which may differ from standard color family names.

    Maximum 75 values.
    """
