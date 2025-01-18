from proxycycle import ProxySet, Proxy, ProxyScrape, Scheme
from proxycycle import filters as pcfilters
import asyncio
import pytest

@pytest.fixture
def proxyset():
    return ProxyScrape.fetch_proxyset(50, schemes = [Scheme.HTTP], max_timeout=300)

def test_DummyUseCheck(proxyset: ProxySet):
    check = pcfilters.DummyUseCheck(timeout=10)

    res = asyncio.run(check.run_async(proxyset))
    assert len(res) != 0

    proxyset.set_proxy(Proxy("127.0.0.2", 9123))
    proxyset.set_proxy(Proxy("127.0.0.2", 9124))
    proxyset.set_proxy(Proxy("127.0.0.2", 9125))
    res2 = asyncio.run(check.run_async(proxyset))

    assert len(res) == len(res2)