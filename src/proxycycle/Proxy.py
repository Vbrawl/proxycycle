from __future__ import annotations
from .enums import Scheme, AnonymityLevel


class Proxy:
    """A class to hold information about a proxy server
    """
    def __init__(self, host:str, port:int, scheme:Scheme|str = Scheme.Undefined, anonymity_level:AnonymityLevel|str = AnonymityLevel.Undefined, country: str | None = None, latency:int = -1):
        """Initialize a proxy instance.

        Args:
            host (str): The hostname or ip address of the proxy server.
            port (int): The port to connect for the proxy service.
            scheme (Scheme | str, optional): The scheme/protocol used for connecting to the proxy. Defaults to Scheme.Undefined.
            anonymity_level (AnonymityLevel | str, optional): The anonymity level of the proxy. Defaults to AnonymityLevel.Undefined.
            latency (int, optional): The latency of the server (At least what we know). Defaults to -1.
        """
        self.host = host
        self.port = port

        self.scheme = scheme if isinstance(scheme, Scheme) else Scheme(scheme)
        self.anonymity_level = anonymity_level if isinstance(anonymity_level, AnonymityLevel) else AnonymityLevel(anonymity_level)
        self.latency = latency
    
    def __repr__(self) -> str:
        return f"%s(host=%s, port=%d, scheme=%s, anonymity_level=%s, latency=%d)" % (
            self.__class__.__qualname__,
            repr(self.host),
            self.port,
            repr(self.scheme.value),
            repr(self.anonymity_level.value),
            self.latency
        )
    
    def __str__(self) -> str:
        return self.toString()

    def __eq__(self, o: object) -> bool:
        """Check if proxy server is identical to another object.

        For this to be true the object needs to:
        1) be a Proxy object
        2) have the same host
        3) have the same port
        4) have the same scheme

        Args:
            o (object): The object to be compared to the proxy.

        Returns:
            bool: Whether the object is equal to the proxy or not.
        """
        if isinstance(o, Proxy):
            return self.host == o.host and self.port == o.port and self.scheme == o.scheme
        return False
    
    def __hash__(self) -> int:
        return hash((self.host, self.port, self.scheme))
    
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
        """Return a string representation of the data.

        Returns:
            str: The string representation of the data.
        """
        string = f"{self.host}:{self.port}"
        if self.scheme != Scheme.Undefined:
            string = self.scheme + "://" + string
        
        return string