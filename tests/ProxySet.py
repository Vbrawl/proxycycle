# import unittest
import pytest
from proxycycle.ProxySet import ProxySet
from proxycycle.Proxy import Proxy
from proxycycle.enums import AnonymityLevel
from io import StringIO

@pytest.fixture
def proxy1():
    return Proxy("127.0.0.1", 8080)

@pytest.fixture
def proxy1alt():
    return Proxy("127.0.0.1", 8080, anonymity_level=AnonymityLevel.Elite)

@pytest.fixture
def proxy2():
    return Proxy("127.0.0.2", 8080)

@pytest.fixture
def proxy2alt():
    return Proxy("127.0.0.2", 8080, anonymity_level=AnonymityLevel.Elite)

@pytest.fixture
def proxy3():
    return Proxy("127.0.0.3", 8080)


def test_set_proxy(proxy1:Proxy, proxy1alt:Proxy, proxy2:Proxy):
    ps = ProxySet([proxy1])
    pslen = len(ps)
    ps.set_proxy(proxy1alt)
    assert len(ps) == pslen
    assert ps[0].anonymity_level == proxy1alt.anonymity_level

    ps.set_proxy(proxy2)
    assert len(ps) == pslen+1

def test_extend_with_proxysets(proxy1:Proxy, proxy1alt:Proxy, proxy2:Proxy, proxy2alt:Proxy, proxy3:Proxy):
    ps = ProxySet([proxy1])
    psextend = ProxySet([proxy1alt, proxy2]) # ProxySet to use for extending ps
    psextend2 = ProxySet([proxy2alt, proxy3])

    ps.extend_with_proxysets(psextend, psextend2)
    assert len(ps) == 3 # the "alt" proxies will just alter the existing entries so we don't count them.

    assert ps[0] == proxy1alt
    assert ps[1] == proxy2alt
    assert ps[2] == proxy3

def test_getitem(proxy1:Proxy, proxy2:Proxy):
    ps = ProxySet([proxy1, proxy2])
    assert ps[0] == proxy1
    assert ps[1] == proxy2

def test_len(proxy1:Proxy, proxy2:Proxy, proxy3:Proxy):
    ps = ProxySet()
    assert len(ps) == 0

    ps.set_proxy(proxy1)
    assert len(ps) == 1

    ps.set_proxy(proxy2)
    assert len(ps) == 2

    ps.set_proxy(proxy3)
    assert len(ps) == 3

def test_iter(proxy1:Proxy, proxy2:Proxy, proxy3:Proxy):
    loop_number = 0
    ps = ProxySet([proxy1, proxy2, proxy3])
    for _ in ps:
        loop_number += 1
    assert loop_number == 3

def test_cycle(proxy1:Proxy, proxy2:Proxy, proxy3:Proxy):
    def cycle_through(pset:ProxySet, divider:int, max_loop:int, conditions:dict[int, Proxy]) -> int:
        i = 0
        for i, p in enumerate(pset.cycle()):
            assert p == conditions[i % divider]
            if i == max_loop: return i
        return i

    ps = ProxySet()
    conditions: dict[int, Proxy] = {}
    max_loop = 0
    
    # 0
    for _ in ps.cycle():
        assert False

    # 1
    ps.set_proxy(proxy1)
    conditions[0] = proxy1
    max_loop = 4 * len(conditions)
    assert cycle_through(ps, 1, max_loop, conditions) == max_loop

    # 2
    ps.set_proxy(proxy2)
    conditions[1] = proxy2
    max_loop = 4 * len(conditions)
    assert cycle_through(ps, 2, max_loop, conditions) == max_loop

    # 3
    ps.set_proxy(proxy3)
    conditions[2] = proxy3
    max_loop = 4 * len(conditions)
    assert cycle_through(ps, 3, max_loop, conditions) == max_loop

def test_fromFile(proxy1:Proxy, proxy2:Proxy, proxy3:Proxy, proxy1alt:Proxy):
    ps = ProxySet([proxy1, proxy2, proxy3])

    fdata = StringIO()
    fdata.write('\n'.join(map(Proxy.toString, ps)))
    fdata.seek(0)

    ps2 = ProxySet.fromFile(fdata)

    assert len(ps) == len(ps2)
    for i, proxy in enumerate(ps):
        assert proxy == ps2[i]