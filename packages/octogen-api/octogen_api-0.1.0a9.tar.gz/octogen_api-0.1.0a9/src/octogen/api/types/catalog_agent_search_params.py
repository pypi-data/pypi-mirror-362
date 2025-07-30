# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["CatalogAgentSearchParams"]


class CatalogAgentSearchParams(TypedDict, total=False):
    text: Required[str]
    """Query text to be input to an LLM to generate a TextSearchQuery object"""

    limit: int
    """The maximum number of results to return from the search."""
