# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["CatalogStyleAndTagsSearchParams"]


class CatalogStyleAndTagsSearchParams(TypedDict, total=False):
    type: Required[str]

    styles: Required[List[str]]

    tags: Required[List[str]]

    compact_mode: Optional[Literal["compact", "medium"]]

    limit: int
