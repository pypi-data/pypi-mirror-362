# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Rating"]


class Rating(BaseModel):
    average_rating: Optional[float] = None
    """Average rating, scaled between 1-5."""

    rating_count: Optional[int] = None
    """Total number of ratings. Must be nonnegative."""

    rating_histogram: Optional[List[int]] = None
    """List of rating counts per rating value."""

    type: Optional[Literal["AggregateRating", "Rating"]] = None
