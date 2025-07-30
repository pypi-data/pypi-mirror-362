# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["ErrorInfo"]


class ErrorInfo(BaseModel):
    code: str
    """A unique error code for programmatic handling."""

    message: str
    """A human-readable error message."""
