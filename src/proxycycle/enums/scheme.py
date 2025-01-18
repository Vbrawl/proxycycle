from __future__ import annotations
from enum import StrEnum


class Scheme(StrEnum):
    Undefined   = "all"
    HTTP        = "http"
    SOCKS4      = "socks4"
    SOCKS5      = "socks5"