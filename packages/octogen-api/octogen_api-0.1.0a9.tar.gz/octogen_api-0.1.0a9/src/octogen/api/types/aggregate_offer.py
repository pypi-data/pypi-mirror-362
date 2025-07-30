# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .offer import Offer
from .._models import BaseModel
from .organization import Organization

__all__ = ["AggregateOffer"]


class AggregateOffer(BaseModel):
    availability: Optional[str] = None
    """
    The availability of the product — for example http://schema.org/InStock,
    http://schema.org/OutOfStock, http://schema.org/PreOrder, etc.
    """

    high_price: Optional[float] = FieldInfo(alias="highPrice", default=None)
    """Highest price of the offers."""

    item_condition: Optional[str] = FieldInfo(alias="itemCondition", default=None)
    """Condition of the items."""

    low_price: Optional[float] = FieldInfo(alias="lowPrice", default=None)
    """Lowest price of the offers."""

    offer_count: Optional[int] = FieldInfo(alias="offerCount", default=None)
    """Number of offers."""

    offers: Optional[List[Offer]] = None
    """List of individual offers."""

    price_currency: Optional[str] = FieldInfo(alias="priceCurrency", default=None)
    """Currency of the offers."""

    seller: Optional[Organization] = None
    """Schema.org model for Organization."""

    type: Optional[str] = FieldInfo(alias="type_", default=None)
