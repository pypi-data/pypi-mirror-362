# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = ["SampleListResponse", "SampleListResponseItem"]


class SampleListResponseItem(BaseModel):
    language: str
    """Primary programming language of the sample."""

    sample_id: str
    """Unique identifier for the sample (e.g., 'traccar-1')."""

    verifier: Literal["test_suite", "static_analysis", "linter", "custom"]
    """The type of verifier used for this sample."""

    created_at: Optional[datetime] = None
    """Timestamp when the sample was created (UTC)."""

    dataset: Optional[str] = None
    """Dataset name for the sample."""

    description: Optional[str] = None
    """A brief description of the sample."""

    latest: Optional[bool] = None
    """Whether this is the latest version."""

    version: Optional[int] = None
    """Version number of the sample."""

    version_description: Optional[str] = None
    """Description of this version."""


SampleListResponse: TypeAlias = List[SampleListResponseItem]
