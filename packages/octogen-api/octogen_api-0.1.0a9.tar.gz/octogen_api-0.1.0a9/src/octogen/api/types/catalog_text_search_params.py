# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

from .facet_param import FacetParam

__all__ = ["CatalogTextSearchParams"]


class CatalogTextSearchParams(TypedDict, total=False):
    text: Required[str]
    """
    The text is converted to a vector embedding and used to search for products in
    the e-commerce catalog with pre-computed product embeddings. It will be matched
    against the embeddings from retrieval_embedding_columns during retrieval.
    """

    exclusion_facets: Optional[Iterable[FacetParam]]
    """Facets that will be excluded from the search results."""

    facets: Optional[Iterable[FacetParam]]
    """The search results will be filtered by the specified facets."""

    limit: int
    """The maximum number of results to return from the search. The default is 10."""

    price_max: Optional[float]
    """
    The products will be filtered to have a price less than or equal to the
    specified value.
    """

    price_min: Optional[float]
    """
    The products will be filtered to have a price greater than or equal to the
    specified value.
    """

    ranking_embedding_columns: Optional[List[Literal["embedding", "style_embedding", "tags_embedding"]]]
    """The columns to use for the ranking embeddings.

    If not specified, defaults to ['embedding']. Pick the column that best
    corresponds to the `ranking_text` parameter.
    """

    ranking_text: Optional[str]
    """The text is converted to a vector embedding and used to rank the search results.

    It will be matched against the embeddings from ranking_embedding_columns during
    ranking.
    """

    retrieval_embedding_columns: Optional[List[Literal["embedding", "style_embedding", "tags_embedding"]]]
    """The columns to use for the retrieval embeddings.

    If not specified, defaults to ['embedding']. Pick the column that best
    corresponds to the `text` parameter.
    """
