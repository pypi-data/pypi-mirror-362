# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Organization", "ContactPoint", "ContactPointAddress"]


class ContactPointAddress(BaseModel):
    address_country: Optional[str] = FieldInfo(alias="addressCountry", default=None)
    """The country."""

    address_locality: Optional[str] = FieldInfo(alias="addressLocality", default=None)
    """The locality."""

    address_region: Optional[str] = FieldInfo(alias="addressRegion", default=None)
    """The region."""

    postal_code: Optional[str] = FieldInfo(alias="postalCode", default=None)
    """The postal code."""

    street_address: Optional[str] = FieldInfo(alias="streetAddress", default=None)
    """The street address."""

    type: Optional[str] = None


class ContactPoint(BaseModel):
    address: Optional[ContactPointAddress] = None
    """Schema.org model for PostalAddress."""

    contact_type: Optional[str] = FieldInfo(alias="contactType", default=None)
    """The type of contact point."""

    email: Optional[str] = None
    """The email address of the contact point."""

    telephone: Optional[str] = None
    """The telephone number of the contact point."""

    type: Optional[str] = None


class Organization(BaseModel):
    contact_point: Optional[ContactPoint] = FieldInfo(alias="contactPoint", default=None)
    """Schema.org model for ContactPoint."""

    context: Optional[str] = None

    logo: Optional[str] = None
    """The logo of the organization."""

    name: Optional[str] = None
    """The name of the organization."""

    same_as: Optional[List[str]] = FieldInfo(alias="sameAs", default=None)
    """The same as of the organization."""

    type: Optional[str] = None

    url: Optional[str] = None
    """The URL of the organization."""
