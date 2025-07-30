# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import date

from pydantic import Field as FieldInfo

from .rating import Rating
from .._models import BaseModel

__all__ = ["Review", "Author"]


class Author(BaseModel):
    name: Optional[str] = None
    """The name of the person."""

    type: Optional[str] = FieldInfo(alias="type_", default=None)


class Review(BaseModel):
    author: Optional[Author] = None
    """Schema.org Person definition."""

    date_published: Optional[date] = FieldInfo(alias="datePublished", default=None)
    """The date the review was published."""

    review_body: Optional[str] = FieldInfo(alias="reviewBody", default=None)
    """The body of the review."""

    review_rating: Optional[Rating] = FieldInfo(alias="reviewRating", default=None)
    """The rating given in this review."""

    type: Optional[str] = FieldInfo(alias="type_", default=None)
