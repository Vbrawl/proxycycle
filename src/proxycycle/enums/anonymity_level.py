from __future__ import annotations
from enum import StrEnum

class AnonymityLevel(StrEnum):
    Undefined   = "all"
    Transparent = "transparent"
    Anonymous   = "anonymous"
    Elite       = "elite"