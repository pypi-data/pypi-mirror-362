# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Brand"]


class Brand(BaseModel):
    name: Optional[str] = None
    """The name of the brand."""

    description: Optional[str] = None
    """Description of the brand."""

    logo: Optional[str] = None
    """URL of the brand's logo."""

    same_as: Optional[List[str]] = FieldInfo(alias="sameAs", default=None)
    """URLs to external references for the brand."""

    type: Optional[str] = FieldInfo(alias="type_", default=None)

    url: Optional[str] = None
    """The brand's official website."""
