from typing import Any
import requests
from urllib.parse import urlencode
from ..ProxySet import ProxySet
from ..Proxy import Proxy
from ..enums.scheme import Scheme
from ..enums.anonymity_level import AnonymityLevel


class ProxyScrape():
    @staticmethod
    def fetch_proxyset(limit:int|None = None, protocols:list[str] = ["socks4", "socks5"], anonymity_levels:list[str] = [], timeout:int|None = None, session:requests.Session|None = None):
        """Fetch a proxy list from the api.proxyscrape.com

        Args:
            limit (int | None, optional): The maximum number of proxies to fetch.
            protocols (list[str], optional): A list of protocols allowed ("http", "socks4", "socks5"). Defaults to ["socks4", "socks5"]. (Disable with [])
            anonymity_levels (list[str], optional): Anonymity level of the proxy. Defaults to [].
            timeout (int | None, optional): The maximum allowed timeout a proxy is allowed to have. Defaults to None.

        Returns:
            ProxySet: An instance of the class that was used to call the function.
        """
        params:dict[str, str|int] = {
            "request": "displayproxies",
            "proxy_format": "protocolipport",
            "format": "json",
        }

        if protocols: params["protocol"] = ','.join(protocols)
        if anonymity_levels: params["anonymity"] = ','.join(anonymity_levels)
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