# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["FileListParams"]


class FileListParams(TypedDict, total=False):
    ending_before: str

    limit: int

    sort_order: Literal["asc", "desc"]

    starting_after: str
