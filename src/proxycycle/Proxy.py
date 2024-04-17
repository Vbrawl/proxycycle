from __future__ import annotations
from .enums import Scheme, AnonymityLevel


class Proxy:
    def __init__(self, host:str, port:int, scheme:Scheme|int = Scheme.Undefined, anonymity_level:AnonymityLevel|int = AnonymityLevel.Undefined, latency:int = -1):
        self.host = host
        self.port = port

        self.scheme = scheme if isinstance(scheme, Scheme) else Scheme(scheme)
        self.anonymity_level = anonymity_level if isinstance(anonymity_level, AnonymityLevel) else AnonymityLevel(anonymity_level)
        self.latency = latency
    
    def __repr__(self) -> str:
        return "%s(host=%s, port=%d, scheme=%d, anonymity_level=%d, latency=%d)" % (
            self.__class__.__qualname__,
            repr(self.host),
            self.port,
            int(self.scheme),
            int(self.anonymity_level),
            self.latency
        )

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Proxy):
            return self.host == o.host and self.port == o.port and self.scheme == o.scheme
        return False