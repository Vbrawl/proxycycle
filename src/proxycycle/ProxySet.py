from __future__ import annotations
from typing import Iterable, Iterator, TYPE_CHECKING, Callable
if TYPE_CHECKING: from _typeshed import SupportsNoArgReadline
from .Proxy import Proxy
import itertools
import warnings

class ProxySet(Iterable):
    """A set-like iterable object to hold multiple proxies.
    """
    def __init__(self, proxies:Iterable[Proxy] = []):
        """Initialize a ProxySet object with proxy servers.

        Args:
            proxies (Iterable[Proxy], optional): An iterable with proxy objects. Defaults to [].
        """
        self._proxies = []
        self.extend_with_proxysets(proxies)

    def set_proxy(self, proxy: Proxy) -> None:
        """Add a proxy to the set or update the proxy if it's already included.

        Args:
            proxy (Proxy): The proxy to be added/updated.
        """
        try:
            index = self._proxies.index(proxy)
            self._proxies[index] = proxy
        except ValueError:
            self._proxies.append(proxy)

    def extend_with_proxysets(self, *proxysets:Iterable[Proxy]|ProxySet):
        """Call set_proxy for all proxies on every proxyset iterable.

        Args:
            *proxysets (Iterable[Proxy]|ProxySet): Iterables containing proxy objects.
        """
        for proxyset in proxysets:
            for proxy in proxyset:
                self.set_proxy(proxy)
    
    def __getitem__(self, key:int) -> Proxy:
        return self._proxies[key]
    
    def __len__(self) -> int:
        return len(self._proxies)
    
    def __iter__(self) -> Iterator[Proxy]:
        return iter(self._proxies)
    
    def cycle(self) -> Iterator[Proxy]:
        """Cycle infinitely through the set (loop to the start when no more proxies exist).

        Returns:
            Iterator[Proxy]: Returns an iterator that loops through the entire set infinitely.
        """
        return itertools.cycle(self._proxies)
    
    def deduplicate(self, select:Callable[[list[Proxy]], Proxy|None] = lambda x: x[0]) -> ProxySet:
        """Remove duplicates of the same host.

        Args:
            select (Callable[[list[Proxy]], Proxy|None], optional): A callable that accepts a list[Proxy] as parameter and returns either a Proxy or None. Defaults to lambdax:x[0].

        Returns:
            ProxySet: A proxy set containing all proxies returned by the "select" callable.
        """
        proxies:dict[str, list[Proxy]] = {}
        proxyset = ProxySet()

        for proxy in self:
            if proxy.host in proxies:
                proxies[proxy.host].append(proxy)
            else:
                proxies[proxy.host] = [proxy]
        
        for proxy in map(select, proxies.values()):
            if proxy is not None:
                proxyset.set_proxy(proxy)

        return ProxySet(proxyset)
    
    @classmethod
    def fromFile(cls, fileR:SupportsNoArgReadline[str]) -> ProxySet:
        """Initialize a ProxySet from a file of proxies.

        Args:
            fileR (SupportsNoArgReadline[str]): An object that supports readline() and has the data for the proxies (a file handle is sufficient).

        Returns:
            ProxySet: The initialized proxyset.
        """
        proxies = []

        while (line := fileR.readline()).strip():
            try:
                proxies.append(Proxy.fromString(line))
            except ValueError as err:
                warnings.warn(str(err), SyntaxWarning)
        return ProxySet(proxies)