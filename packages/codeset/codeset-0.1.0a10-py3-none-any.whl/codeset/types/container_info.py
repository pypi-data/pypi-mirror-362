# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from .._models import BaseModel

__all__ = ["ContainerInfo"]


class ContainerInfo(BaseModel):
    container_name: str
    """Name of the Cloud Run service."""

    created_at: datetime
    """Timestamp when the container was created (UTC)."""

    expires_at: datetime
    """Timestamp when the container will expire (UTC)."""

    sample_id: str
    """Sample ID of the container."""

    service_url: str
    """URL of the Cloud Run service."""

    status: str
    """Status of the container."""
