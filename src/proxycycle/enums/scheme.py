from enum import IntFlag, auto


class Scheme(IntFlag):
    Undefined = 0
    HTTP      = auto()
    SOCKS4    = auto()
    SOCKS5    = auto()