# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["Audience"]


class Audience(BaseModel):
    age_groups: List[str]
    """The age groups of the audience.

    Suggested values: 'newborn', 'infant', 'toddler', 'kids', 'adult'. Maximum 5
    values.
    """

    genders: List[str]
    """The genders of the audience.

    Suggested values: 'male', 'female', 'unisex'. Maximum 5 values.
    """
