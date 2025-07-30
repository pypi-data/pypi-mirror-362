# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

__all__ = ["FacetParam"]


class FacetParam(TypedDict, total=False):
    name: Required[Literal["brand_name", "product_type", "gender"]]
    """The facet to filter by.

    Options: brand_name (The brand or manufacturer name of the product),
    product_type (The type or category of the product (e.g., shirt, pants, shoes)),
    gender (The target gender for the product (e.g., men, women, unisex))
    """

    values: Required[List[str]]
    """List of values to filter by.

    They should all be lowercase. Facet values can be phrases, so make sure to
    include the spaces.
    """
