# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["FileScrapeWebParams"]


class FileScrapeWebParams(TypedDict, total=False):
    url: Required[str]
    """URL to scrape"""
