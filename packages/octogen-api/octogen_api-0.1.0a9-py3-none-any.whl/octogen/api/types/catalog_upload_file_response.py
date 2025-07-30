# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["CatalogUploadFileResponse"]


class CatalogUploadFileResponse(BaseModel):
    file_id: str

    file_url: Optional[str] = None
