"""
Generic auth helpers - Python-based.
Parses challenge-style login URLs (query params only). No external tokens stored.
"""

from urllib.parse import urlparse, parse_qs
from dataclasses import dataclass
from typing import Optional


@dataclass
class LoginParams:
    """Parsed login URL parameters."""

    challenge: Optional[str] = None
    uuid: Optional[str] = None
    mode: Optional[str] = None

    @classmethod
    def from_url(cls, url: str) -> "LoginParams":
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        return cls(
            challenge=qs.get("challenge", [None])[0],
            uuid=qs.get("uuid", [None])[0],
            mode=qs.get("mode", [None])[0],
        )


def parse_login_url(url: str) -> LoginParams:
    """Parse a login/deep-control URL and return query params. Does not store or use tokens."""
    return LoginParams.from_url(url)
