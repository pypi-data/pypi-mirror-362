# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["FulfillmentInfo"]


class FulfillmentInfo(BaseModel):
    place_ids: str
    """Store or region IDs for the fulfillment type.

    Must match the pattern '[a-zA-Z0-9_-]'.
    """

    type: str
    """
    Fulfillment type such as 'pickup-in-store', 'same-day-delivery', or a custom
    type.
    """
