# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["QuantitativeValue"]


class QuantitativeValue(BaseModel):
    unit_code: Optional[str] = FieldInfo(alias="unitCode", default=None)
    """
    The unit of measurement given using the UN/CEFACT Common Code (3 characters) or
    a URL. Other codes than the UN/CEFACT Common Code may be used with a prefix
    followed by a colon..
    """

    value: Optional[float] = None
    """The value of the quantitative value."""
