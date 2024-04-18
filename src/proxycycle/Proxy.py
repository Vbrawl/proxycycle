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
    
    def __hash__(self) -> int:
        return hash((self.host, self.port,))
    
    @classmethod
    def fromString(cls, string:str) -> Proxy:
        """Construct a Proxy object from the given string.
        Valid formats for the string:
        * scheme://host:port
        * host:port
        * scheme://[IPv6]:port
        * [IPv6]:port

        Args:
            string (str): The host string to parse.

        Raises:
            ValueError: When a component from the string is not valid.

        Returns:
            Proxy: A Proxy object containing information from the string.
        """
        scheme = Scheme.Undefined
        host:str = ""
        port:int = -1

        # Supported format: scheme://host:port
        # Supported format (IPv6): scheme://[IPv6]:port
        if "://" in string:
            temp, string = string.split('://', maxsplit=1)
            try:
                scheme = {
                    "http": Scheme.HTTP,
                    "socks4": Scheme.SOCKS4,
                    "socks5": Scheme.SOCKS5
                }[temp.lower()]
            except KeyError:
                raise ValueError(f"scheme({temp}) doesn't seem to be a valid scheme.")
        
        if string[0] == '[':
            host, string = string.split(']', maxsplit=1)
        elif ":" in string:
            host, string = string.split(':', maxsplit=1)
        else:
            host = string
        
        if string != '':
            try:
                port = int(string)
            except ValueError:
                raise ValueError(f"port({string}) doesn't seem to be a valid port.")
        
        if host != '' and port >= 0:
            return Proxy(host, port, scheme)
        else:
            raise ValueError(f"string({string}) doesn't seem to be a valid proxy server.")
    
    def toString(self) -> str:
        string = f"{self.host}:{self.port}"
        try:
            schemeName = {
                Scheme.HTTP: "http",
                Scheme.SOCKS4: "socks4",
                Scheme.SOCKS5: "socks5"
            }[self.scheme]
            string = schemeName + '://' + string
        except KeyError:
            pass # Silent
        
        return string