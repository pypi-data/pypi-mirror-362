# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .offer import Offer
from .._models import BaseModel

__all__ = ["Offers"]


class Offers(BaseModel):
    item_condition: Optional[str] = FieldInfo(alias="itemCondition", default=None)
    """The condition of the product (e.g., NewCondition, UsedCondition)."""

    offers: Optional[List[Offer]] = None
    """A list of individual offers for the product."""

    url: Optional[str] = None
    """The URL where the product can be purchased."""
