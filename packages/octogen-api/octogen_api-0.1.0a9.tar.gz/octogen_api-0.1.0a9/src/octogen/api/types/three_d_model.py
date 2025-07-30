# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ThreeDModel", "Encoding"]


class Encoding(BaseModel):
    content_url: Optional[str] = FieldInfo(alias="contentUrl", default=None)
    """URL to the actual content of the media object."""

    context: Optional[str] = None

    encoding_format: Optional[str] = FieldInfo(alias="encodingFormat", default=None)
    """The media format or mime type."""

    name: Optional[str] = None
    """The name of the media object."""

    type: Optional[str] = FieldInfo(alias="type_", default=None)

    upload_date: Optional[str] = FieldInfo(alias="uploadDate", default=None)
    """The date the media was uploaded."""


class ThreeDModel(BaseModel):
    author: Optional[str] = None
    """Author of the work."""

    content_size: Optional[str] = FieldInfo(alias="contentSize", default=None)
    """File size in megabytes or gigabytes."""

    content_url: Optional[str] = FieldInfo(alias="contentUrl", default=None)
    """URL to the actual content of the media object."""

    context: Optional[str] = None

    creator: Optional[str] = None
    """The creator of the 3D model."""

    date_published: Optional[str] = FieldInfo(alias="datePublished", default=None)
    """Date of first publication."""

    embed_url: Optional[str] = FieldInfo(alias="embedUrl", default=None)
    """A URL pointing to a player for the 3D model."""

    encoding: Optional[List[Encoding]] = None
    """A media object representing the 3D model."""

    encoding_format: Optional[str] = FieldInfo(alias="encodingFormat", default=None)
    """The file format of the 3D model (e.g., 'model/gltf+json')."""

    interaction_count: Optional[int] = FieldInfo(alias="interactionCount", default=None)
    """Number of interactions for the 3D model."""

    is_based_on_url: Optional[str] = FieldInfo(alias="isBasedOnUrl", default=None)
    """A related resource that the 3D model is based on."""

    license: Optional[str] = None
    """License under which the work is published."""

    material: Optional[str] = None
    """The material used to create the 3D model."""

    name: Optional[str] = None
    """The name of the media object."""

    thumbnail_url: Optional[List[str]] = FieldInfo(alias="thumbnailUrl", default=None)
    """A URL pointing to the model thumbnail image."""

    type: Optional[str] = FieldInfo(alias="type_", default=None)

    upload_date: Optional[str] = FieldInfo(alias="uploadDate", default=None)
    """The date the media was uploaded."""
