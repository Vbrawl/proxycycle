from typing import Callable
from proxycycle import ProxySet
from proxycycle.api import ProxyScrape
from proxycycle.enums import Scheme, AnonymityLevel
import argparse

def output__scheme_ip_port(pset:ProxySet):
    for p in pset:
        print(p)

def fetch_proxy():
    arg_parts:set[str]
    available_schemes:dict[str, Scheme] = {
        "socks5":           Scheme.SOCKS5,
        "socks4":           Scheme.SOCKS4,
        "http":             Scheme.HTTP
    }

    available_anonymitylevels:dict[str, AnonymityLevel] = {
        "elite":            AnonymityLevel.Elite,
        "anonymous":        AnonymityLevel.Anonymous,
        "transparent":      AnonymityLevel.Transparent
    }

    available_outformats:dict[str, Callable[[ProxySet], None]] = {
        "scheme-ip-port":   output__scheme_ip_port
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", default=1, type=int, help="The number of proxies to fetch. For leaving the decision up to the API provider use 0. [Default=1]", dest="count")
    parser.add_argument("-s", "--scheme", default="socks5,socks4,http", help=f"A comma-separated list of schemes that should be allowed. Available Options: {','.join(available_schemes.keys())} [Default=socks5,socks4,http]", dest="scheme")
    parser.add_argument("-a", "--anonymity", default="elite,anonymous,transparent", help=f"A comma-separated list of anonymity levels that should be allowed. Available Options: {','.join(available_anonymitylevels.keys())} [Default=elite,anonymous,transparent]", dest="anonymity_level")
    parser.add_argument("-t", "--max-timeout", default=0, type=int, help="The maximum timeout of a proxy. For no timeout use 0. [Default=0]", dest="max_timeout")
    parser.add_argument("-f", "--format", default="scheme-ip-port", help="The output format of the data. [Default=scheme-ip-port]", choices=available_outformats.keys(), dest="out_format")
    args = parser.parse_args()

    # Extract arguments
    out_format = args.out_format

    # Parse count
    count:int|None
    if args.count < 0:
        raise ValueError("Fetch count must be >=0")
    elif args.count == 0:
        count = None
    else:
        count = args.count
    
    # Parse max_timeout
    max_timeout:int|None
    if args.max_timeout < 0:
        raise ValueError("Max Timeout must be >=0")
    elif args.max_timeout == 0:
        max_timeout = None
    else:
        max_timeout = args.max_timeout

    ## Parse scheme
    scheme = Scheme.Undefined
    arg_parts = set(args.scheme.split(','))

    for s in arg_parts:
        if s not in available_schemes:
            raise KeyError(f"Requested scheme not found: {s}")
        scheme |= available_schemes[s]

    ## Parse anonymity level
    anonymity_level = AnonymityLevel.Undefined
    arg_parts = set(args.anonymity_level.split(','))

    for s in arg_parts:
        if s not in available_anonymitylevels:
            raise KeyError(f"Requested anonymity level not found: {s}")
        anonymity_level |= available_anonymitylevels[s]

    # Fetch proxies
    api = ProxyScrape()
    pset = api.fetch_proxyset(count, scheme, anonymity_level, max_timeout)

    # Output proxies
    available_outformats[out_format](pset)