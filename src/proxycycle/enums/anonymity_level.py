from enum import IntFlag, auto


class AnonymityLevel(IntFlag):
    Undefined   = 0
    Transparent = auto()
    Anonymous   = auto()
    Elite       = auto()