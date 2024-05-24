import pytest
from proxycycle.Proxy import Proxy
from proxycycle.enums.scheme import Scheme

@pytest.fixture
def proxy_list():
    return [
        Proxy(host="127.0.0.1", port=8080),
        Proxy(host="127.0.0.0", port=8888),
        Proxy(host="127.0.0.1", port=8081),
        Proxy(host="127.0.0.1", port=8080),
        Proxy(host="127.0.0.1", port=8080, scheme=Scheme.HTTP)
    ]

def test_repr(proxy_list:list[Proxy]):
    assert proxy_list[0] == eval(repr(proxy_list[0]))
    assert proxy_list[1] == eval(repr(proxy_list[1]))

def test_compare(proxy_list:list[Proxy]):
    assert proxy_list[0] == proxy_list[0]
    assert proxy_list[0] != proxy_list[1]
    assert proxy_list[0] != proxy_list[2]
    assert proxy_list[0] == proxy_list[3]

def test_hash(proxy_list:list[Proxy]):
    assert hash(proxy_list[0]) == hash(proxy_list[0])
    assert hash(proxy_list[0]) != hash(proxy_list[1])
    assert hash(proxy_list[0]) != hash(proxy_list[2])
    assert hash(proxy_list[0]) == hash(proxy_list[3])
    assert hash(proxy_list[0]) != hash(proxy_list[4])

def test_strings(proxy_list:list[Proxy]):
    assert proxy_list[0] == proxy_list[0].fromString(proxy_list[0].toString())
    assert proxy_list[1] == proxy_list[1].fromString(proxy_list[1].toString())
    assert proxy_list[2] == proxy_list[2].fromString(proxy_list[2].toString())
    assert proxy_list[3] == proxy_list[3].fromString(proxy_list[3].toString())