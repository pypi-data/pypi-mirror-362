# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .context_enum import ContextEnum

__all__ = ["BreadcrumbList", "ItemListElement", "ItemListElementItem"]


class ItemListElementItem(BaseModel):
    id: str = FieldInfo(alias="id_")

    name: str


class ItemListElement(BaseModel):
    item: ItemListElementItem

    position: int

    type: str = FieldInfo(alias="type_")


class BreadcrumbList(BaseModel):
    context: Optional[ContextEnum] = None

    item_list_element: Optional[List[ItemListElement]] = FieldInfo(alias="itemListElement", default=None)
    """The list of breadcrumb items."""

    type: Optional[str] = FieldInfo(alias="type_", default=None)
