# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .vector_store_file_status import VectorStoreFileStatus

__all__ = ["VectorStoreFile"]


class VectorStoreFile(BaseModel):
    id: str
    """Unique identifier for the file"""

    filename: Optional[str] = None
    """Name of the file"""

    metadata: Optional[object] = None
    """Optional file metadata"""

    status: Optional[VectorStoreFileStatus] = None
    """Processing status of the file"""

    last_error: Optional[object] = None
    """Last error message if processing failed"""

    vector_store_id: str
    """ID of the containing vector store"""

    created_at: datetime
    """Timestamp of vector store file creation"""

    version: Optional[int] = None
    """Version number of the file"""

    usage_bytes: Optional[int] = None
    """Storage usage in bytes"""

    object: Optional[Literal["vector_store.file"]] = None
    """Type of the object"""
