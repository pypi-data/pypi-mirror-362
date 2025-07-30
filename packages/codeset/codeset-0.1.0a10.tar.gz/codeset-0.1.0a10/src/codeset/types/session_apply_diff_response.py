# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["SessionApplyDiffResponse"]


class SessionApplyDiffResponse(BaseModel):
    message: str
    """Details about the diff application."""

    success: bool
    """Whether the diff was applied successfully."""
