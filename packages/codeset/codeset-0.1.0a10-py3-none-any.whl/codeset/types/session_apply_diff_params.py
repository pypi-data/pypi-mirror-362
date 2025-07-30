# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SessionApplyDiffParams"]


class SessionApplyDiffParams(TypedDict, total=False):
    diff: Required[str]
    """The diff to be applied, in unified format."""
