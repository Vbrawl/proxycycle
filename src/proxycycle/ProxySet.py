from __future__ import annotations
from typing import Iterable, Iterator, TYPE_CHECKING
if TYPE_CHECKING: from _typeshed import SupportsNoArgReadline
from .Proxy import Proxy
import itertools
import warnings

class ProxySet(Iterable):
    def __init__(self, proxies:Iterable[Proxy] = []):
        self._proxies = []
        self.extend_with_proxysets(proxies)

    def set_proxy(self, proxy: Proxy) -> None:
        try:
            index = self._proxies.index(proxy)
            self._proxies[index] = proxy
        except ValueError:
            self._proxies.append(proxy)

    def extend_with_proxysets(self, *proxysets:Iterable[Proxy]|ProxySet):
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
        return itertools.cycle(self._proxies)
    
    @classmethod
    def fromFile(cls, fileR:SupportsNoArgReadline[str]) -> ProxySet:
        proxies = []

        while (line := fileR.readline()).strip():
            try:
                proxies.append(Proxy.fromString(line))
            except ValueError as err:
                warnings.warn(str(err), SyntaxWarning)
        return ProxySet(proxies)