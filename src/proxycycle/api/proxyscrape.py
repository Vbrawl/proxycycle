from typing import Any
import requests
from urllib.parse import urlencode
from ..ProxySet import ProxySet
from ..Proxy import Proxy
from ..enums.scheme import Scheme
from ..enums.anonymity_level import AnonymityLevel


class ProxyScrape():
    @staticmethod
    def fetch_proxyset(limit:int|None = None, offset:int|None = None, schemes: list[Scheme] = [Scheme.Undefined], anonymity_levels: list[AnonymityLevel] = [AnonymityLevel.Undefined], countries: list[str] = ["all"], max_timeout:int|None = None):
        """Fetch a proxy list from the api.proxyscrape.com

        Args:
            limit (int | None, optional): The maximum number of proxies to fetch.
            offset (int | None, optional): The number of proxies to skip before fetch.
            schemes (list[Scheme], optional): All schemes that should be accepted. (eg, [Scheme.HTTP, Scheme.SOCKS4], would accept both http and socks4). Defaults to [Scheme.ALL]. (disabled)
            anonymity_levels (list[AnonymityLevel], optional): Anonymity levels that should be accepted. (eg, [AnonymityLevel.Elite, AnonymityLevel.Anonymous], would accept both elite and anonymous). Defaults to [AnonymityLevel.ALL] (disabled).
            countries (list[str], optional): The country codes or "all" for all countries. Defaults to "all".
            max_timeout (int | None, optional): The maximum allowed timeout a proxy is allowed to have. Defaults to None.

        Returns:
            ProxySet: An instance of the class that was used to call the function.
        """
        params:dict[str, str|int] = {
            "request": "displayproxies",
            "proxy_format": "protocolipport",
            "format": "json",
        }

        if limit is not None: params["limit"] = limit
        if offset is not None: params["offset"] = offset
        if max_timeout is not None: params["timeout"] = max_timeout

        if schemes: params["protocol"] = ','.join(schemes)
        if anonymity_levels: params["anonymity"] = ','.join(anonymity_levels)
        if countries: params["country"] = ','.join(countries)

        apiURL = "https://api.proxyscrape.com/v3/free-proxy-list/get?" + urlencode(params)
        try:
            resp = requests.get(apiURL)
            return ProxySet(map(ProxyScrape.parse_proxy_data, resp.json()["proxies"]))
        except Exception:
            return ProxySet()
    
    @staticmethod
    def parse_proxy_data(data:dict[str, Any]) -> Proxy:
        scheme = Scheme(data["protocol"])
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