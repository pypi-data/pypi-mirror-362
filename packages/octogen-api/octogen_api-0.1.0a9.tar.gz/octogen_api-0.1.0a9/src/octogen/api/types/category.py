# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["Category"]


class Category(BaseModel):
    name: str

    url: Optional[str] = None
