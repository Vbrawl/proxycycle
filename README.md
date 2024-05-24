# ProxyCycle

[![PyPI - Version](https://img.shields.io/pypi/v/proxycycle.svg)](https://pypi.org/project/proxycycle)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/proxycycle.svg)](https://pypi.org/project/proxycycle)

-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install proxycycle
```

## Usage

```python
### Initialize a proxy object
from proxycycle.Proxy import Proxy
from proxycycle.enums.scheme import Scheme
from proxycycle.enums.anonymity_level import AnonymityLevel
proxy1 = Proxy("127.0.0.1", 8080)
proxy2 = Proxy("127.0.0.1", 8080, Scheme.HTTP)
proxy3 = Proxy("127.0.0.1", 8080, anonymity_level=AnonymityLevel.Elite)
proxy4 = Proxy("127.0.0.1", 8080, Scheme.HTTP, AnonymityLevel.Elite)
proxy5 = Proxy.fromString("127.0.0.1:8080")
proxy6 = Proxy.fromString("http://127.0.0.1:8080")

### Initialize a proxyset
from proxycycle.ProxySet import ProxySet

ps1 = ProxySet([proxy2, proxy3, proxy4])

ps2 = ProxySet()
ps2.set_proxy(proxy1)

ps3 = ProxySet()
ps3.extend_with_proxysets(ps1, ps2)

with open('file.txt', 'r') as f:
    ps4 = ProxySet.fromFile(f)

### Initialize a proxyset without pre-known proxies
from proxycycle.api.proxyscrape import ProxyScrape
ps5 = ProxyScrape.fetch_proxyset(50)
len(ps5) # less or equal to 50   ^^ (this 50)

### Sometimes a single host can have multiple proxy servers
### In that case we can filter out some of the proxy entries.
from functools import partial

# Get the first (by index) proxy
ps1_deduplicated = ps1.deduplicate()

# Get proxies with port number > 8080
ps1_8080 = ps1.deduplicate(partial(filter, lambda x: x.port > 8080))

# Get the proxy with the highest anonymity level
def select_highest_anonymity_proxy(proxylist:list[Proxy]):
    proxy:Proxy|None = None
    for p in proxylist:
        if proxy is None:
            proxy = p
        elif p.anonymity_level > proxy.anonymity_level:
            proxy = p
    return proxy

ps1_highest_anonymity = ps1.deduplicate(select_highest_anonymity_proxy)
```

## License

`proxycycle` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
