# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .context_enum import ContextEnum

__all__ = ["VideoObject"]


class VideoObject(BaseModel):
    content_url: Optional[str] = FieldInfo(alias="contentUrl", default=None)
    """A URL pointing to the actual video content."""

    context: Optional[ContextEnum] = None

    description: Optional[str] = None
    """The description of the video."""

    duration: Optional[str] = None
    """The duration of the video in ISO 8601 format."""

    embed_url: Optional[str] = FieldInfo(alias="embedUrl", default=None)
    """A URL pointing to a player for the video."""

    interaction_count: Optional[int] = FieldInfo(alias="interactionCount", default=None)
    """The number of interactions for the video."""

    name: Optional[str] = None
    """The name of the video."""

    thumbnail_url: Optional[List[str]] = FieldInfo(alias="thumbnailUrl", default=None)
    """A URL pointing to the video thumbnail image."""

    type: Optional[str] = None

    upload_date: Optional[str] = FieldInfo(alias="uploadDate", default=None)
    """The date when the video was uploaded."""
