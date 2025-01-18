from .Proxy import Proxy
from .ProxySet import ProxySet

class SynchronousCheck:
    def check(self, proxy: Proxy) -> bool:
        raise NotImplementedError()
    
    def run(self, proxyset: ProxySet) -> ProxySet:
        raise NotImplementedError()

class AsynchronousCheck:
    async def check_async(self, proxy: Proxy) -> bool:
        raise NotImplementedError()
    
    async def run_async(self, proxyset: ProxySet) -> ProxySet:
        raise NotImplementedError()



class DummyUseCheck(SynchronousCheck, AsynchronousCheck):
    def __init__(self, url: str = "https://google.com", timeout: float = 3):
        self.url = url
        self.timeout = timeout
    
    def check(self, proxy: Proxy) -> bool:
        import requests
        try:
            resp = requests.get(self.url, timeout=self.timeout, proxies={
                "http": proxy.toString(),
                "https": proxy.toString()
            })
            return resp.status_code == 200
        except Exception:
            pass
        return False
    
    async def check_async(self, proxy: Proxy) -> bool:
        import aiohttp
        from aiohttp_socks import ProxyConnector
        try:
            con = ProxyConnector.from_url(proxy.toString())
            async with aiohttp.ClientSession(connector=con, timeout=aiohttp.ClientTimeout(self.timeout)) as cs:
                async with cs.get(self.url):
                    return True
        except Exception:
            pass
        return False
    
    def run(self, proxyset: ProxySet) -> ProxySet:
        return proxyset.filter(self.check)
    
    async def run_async(self, proxyset: ProxySet) -> ProxySet:
        return await proxyset.filter_async(self.check_async)