# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["Image"]


class Image(BaseModel):
    url: str
    """Required.

    URI of the image. Must be a valid UTF-8 encoded URI with a maximum length of
    5000 characters.
    """

    gs_url: Optional[str] = None
    """Optional URL with the location of the image on google storage"""

    height: Optional[int] = None
    """Height of the image in pixels. Must be nonnegative."""

    size: Optional[int] = None
    """Size of the image in bytes. Must be nonnegative."""

    width: Optional[int] = None
    """Width of the image in pixels. Must be nonnegative."""
