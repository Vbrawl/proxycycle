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
######  Simple  ######

import proxycycle as pc
from proxycycle import filters as pcfilters
import requests

# Fetch proxies
pset = pc.ProxyScrape.fetch_proxyset(50, scheme = pc.Scheme.HTTP, timeout=300)

# Filter proxies
pset_filtered = pcfilters.DummyUseCheck(timeout=10).run(pset)
# Some checks support asyncio:
# pset_filtered = asyncio.run(pcfilters.DummyUseCheck(timeout=10).run_async(pset))

# Loop from start to end, then exit the loop
for proxy in pset_filtered:
    proxy_dict = {
        "http": proxy.toString(),
        "https": proxy.toString()
    }

    # request through proxy
    resp = requests.get(url, proxies = proxy_dict)

# Loop from start to end, forever, exit the loop only if/when there are no more proxies
for proxy in pset_filtered.cycle():
    proxy_dict = {
        "http": proxy.toString(),
        "https": proxy.toString()
    }
    resp = requests.get(url, proxies = proxy_dict)


###### Advanced ######

### Initialize a proxy object
from proxycycle.Proxy import Proxy
proxy1 = Proxy("127.0.0.1", 8080)
proxy2 = Proxy.fromString("127.0.0.1:8080")
proxy3 = Proxy.fromString("http://127.0.0.1:8080")

### Initialize a proxyset (manually)
from proxycycle.ProxySet import ProxySet
ps1 = ProxySet([proxy2, proxy3])

### Initialize a proxyset (from file)
with open('file.txt', 'r') as f:
    ps2 = ProxySet.fromFile(f)

### Initialize a proxyset (automatically)
from proxycycle.api.proxyscrape import ProxyScrape
ps3 = ProxyScrape.fetch_proxyset(limit = 50)

# Add a proxy to a proxyset
ps4 = ProxySet()
ps4.set_proxy(proxy1)

# Extend proxyset with other proxysets (ps4 = ps4 + ps1 + ps2 + ps3)
ps4.extend_with_proxysets(ps1, ps2, ps3)

# Filtering (Using .filter())
ps5 = ps4.filter(lambda p: p.scheme == Scheme.HTTP)

# Filtering (Using .filter_async())
import asyncio
async def check(p):
    import aiohttp
    try:
        async with aiohttp.ClientSession(proxy = p.toString()) as c:
            async with c.get(url) as resp:
                return True
    except Exception:
        return False
ps6 = asyncio.run(ps4.filter_async(check))
```

## License

`proxycycle` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
