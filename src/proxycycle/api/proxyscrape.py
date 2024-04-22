from typing import Any
import requests
from urllib.parse import urlencode
from ..ProxySet import ProxySet
from ..Proxy import Proxy
from ..enums.scheme import Scheme
from ..enums.anonymity_level import AnonymityLevel


class ProxyScrape():
    @staticmethod
    def fetch_proxyset(limit:int|None = None, scheme:Scheme = Scheme.SOCKS4 | Scheme.SOCKS5, anonymity_level:AnonymityLevel = AnonymityLevel.Undefined, timeout:int|None = None, session:requests.Session|None = None):
        """Fetch a proxy list from the api.proxyscrape.com

        Args:
            limit (int | None, optional): The maximum number of proxies to fetch.
            scheme (Scheme, optional): All schemes that should be accepted. (eg, Scheme.HTTP | Scheme.SOCKS4, would accept both http and socks4). Defaults to Scheme.SOCKS4|Scheme.SOCKS5. (Disable with Scheme.Undefined)
            anonymity_level (AnonymityLevel, optional): Anonymity levels that should be accepted. (eg, AnonymityLevel.Elite | AnonymityLevel.Anonymous, would accept both elite and anonymous). Defaults to AnonymityLevel.Undefined (disabled).
            timeout (int | None, optional): The maximum allowed timeout a proxy is allowed to have. Defaults to None.

        Returns:
            ProxySet: An instance of the class that was used to call the function.
        """
        params:dict[str, str|int] = {
            "request": "displayproxies",
            "proxy_format": "protocolipport",
            "format": "json",
        }

        if scheme != Scheme.Undefined:
            protocols = []
            if scheme & Scheme.HTTP: protocols.append("http")
            if scheme & Scheme.SOCKS4: protocols.append("socks4")
            if scheme & Scheme.SOCKS5: protocols.append("socks5")
            params["protocol"] = ','.join(protocols)
        if anonymity_level != AnonymityLevel.Undefined:
            anonymity_levels = []
            if anonymity_level & AnonymityLevel.Transparent: anonymity_levels.append("transparent")
            if anonymity_level & AnonymityLevel.Anonymous: anonymity_levels.append("anonymous")
            if anonymity_level & AnonymityLevel.Elite: anonymity_levels.append("elite")
            params["anonymity"] = ','.join(anonymity_levels)
        if timeout is not None: params["timeout"] = timeout
        if limit is not None: params["limit"] = limit

        apiURL = "https://api.proxyscrape.com/v3/free-proxy-list/get?" + urlencode(params)
        try:
            resp = (session if session is not None else requests).get(apiURL)
            return ProxySet(map(ProxyScrape.parse_proxy_data, resp.json()["proxies"]))
        except Exception:
            return ProxySet()
    
    @staticmethod
    def parse_proxy_data(data:dict[str, Any]) -> Proxy:
        scheme = {
            "http": Scheme.HTTP,
            "socks4": Scheme.SOCKS4,
            "socks5": Scheme.SOCKS5
        }[data['protocol']]

        anonymity_level = {
            "transparent": AnonymityLevel.Transparent,
            "anonymous": AnonymityLevel.Anonymous,
            "elite": AnonymityLevel.Elite
        }[data['anonymity']]

        return Proxy(
                data['ip'],
                data['port'],
                scheme,
                anonymity_level,
                data['timeout'])