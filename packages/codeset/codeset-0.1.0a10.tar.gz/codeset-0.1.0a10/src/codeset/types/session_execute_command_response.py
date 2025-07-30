# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["SessionExecuteCommandResponse"]


class SessionExecuteCommandResponse(BaseModel):
    execution_time_seconds: float
    """Execution time in seconds."""

    exit_code: int
    """Exit code of the executed command."""

    stderr: str
    """Standard error from the command."""

    stdout: str
    """Standard output from the command."""
