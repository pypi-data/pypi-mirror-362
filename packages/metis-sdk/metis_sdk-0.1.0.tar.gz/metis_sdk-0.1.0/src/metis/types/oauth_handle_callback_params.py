# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["OAuthHandleCallbackParams"]


class OAuthHandleCallbackParams(TypedDict, total=False):
    code: Required[str]
    """Authorization code"""

    state: Required[str]
    """OAuth state parameter"""

    error: str
    """OAuth error"""
