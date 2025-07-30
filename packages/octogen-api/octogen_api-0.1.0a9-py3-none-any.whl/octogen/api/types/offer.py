# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .organization import Organization
from .quantitative_value import QuantitativeValue

__all__ = [
    "Offer",
    "PriceSpecification",
    "PriceSpecificationPriceSpecification",
    "PriceSpecificationCompoundPriceSpecification",
    "PriceSpecificationCompoundPriceSpecificationPriceComponent",
]


class PriceSpecificationPriceSpecification(BaseModel):
    price: Optional[float] = None
    """Price of the offer."""

    price_currency: Optional[str] = FieldInfo(alias="priceCurrency", default=None)
    """Currency of the price."""

    valid_from: Optional[str] = FieldInfo(alias="validFrom", default=None)
    """The start of the validity period for the price."""

    valid_through: Optional[str] = FieldInfo(alias="validThrough", default=None)
    """The end of the validity period for the price."""


class PriceSpecificationCompoundPriceSpecificationPriceComponent(BaseModel):
    price: Optional[float] = None
    """Price of the offer."""

    price_currency: Optional[str] = FieldInfo(alias="priceCurrency", default=None)
    """Currency of the price."""

    price_type: Optional[str] = FieldInfo(alias="priceType", default=None)
    """
    The type of price specification as enumerated in schema.org's
    PriceTypeEnumeration, for example http://schema.org/ListPrice,
    http://schema.org/RegularPrice, http://schema.org/SalePrice, etc.
    """

    valid_from: Optional[str] = FieldInfo(alias="validFrom", default=None)
    """The start of the validity period for the price."""

    valid_through: Optional[str] = FieldInfo(alias="validThrough", default=None)
    """The end of the validity period for the price."""


class PriceSpecificationCompoundPriceSpecification(BaseModel):
    price_component: Optional[List[PriceSpecificationCompoundPriceSpecificationPriceComponent]] = FieldInfo(
        alias="priceComponent", default=None
    )
    """A list of unit price specifications for the item or offer."""


PriceSpecification: TypeAlias = Union[
    PriceSpecificationPriceSpecification, PriceSpecificationCompoundPriceSpecification, None
]


class Offer(BaseModel):
    availability: Optional[str] = None
    """
    The availability of the product — for example http://schema.org/InStock,
    http://schema.org/OutOfStock, http://schema.org/PreOrder, etc.
    """

    availability_ends: Optional[str] = FieldInfo(alias="availabilityEnds", default=None)
    """End time of availability."""

    availability_starts: Optional[str] = FieldInfo(alias="availabilityStarts", default=None)
    """Start time of availability."""

    eligible_quantity: Optional[QuantitativeValue] = FieldInfo(alias="eligibleQuantity", default=None)
    """Schema.org QuantitativeValue model."""

    inventory_level: Optional[QuantitativeValue] = FieldInfo(alias="inventoryLevel", default=None)
    """Schema.org QuantitativeValue model."""

    item_condition: Optional[str] = FieldInfo(alias="itemCondition", default=None)
    """Condition of the item."""

    name: Optional[str] = None
    """Name of the offer."""

    price_specification: Optional[PriceSpecification] = FieldInfo(alias="priceSpecification", default=None)
    """Price specification for the product."""

    seller: Optional[Organization] = None
    """Schema.org model for Organization."""

    sku: Optional[str] = None
    """SKU of the product."""

    type: Optional[str] = FieldInfo(alias="type_", default=None)
