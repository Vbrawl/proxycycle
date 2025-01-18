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

    available_outformats:dict[str, Callable[[ProxySet], None]] = {
        "scheme-ip-port":   output__scheme_ip_port
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", default=1, type=int, help="The number of proxies to fetch. For leaving the decision up to the API provider use 0. [Default=1]", dest="count")
    parser.add_argument("-s", "--scheme", default="socks5,socks4,http", help=f"A comma-separated list of schemes that should be allowed. Available Options: {','.join([e.value for e in Scheme])} [Default=all]", dest="scheme")
    parser.add_argument("-a", "--anonymity", default="elite,anonymous,transparent", help=f"A comma-separated list of anonymity levels that should be allowed. Available Options: {','.join([e.value for e in AnonymityLevel])} [Default=all]", dest="anonymity_level")
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
    arg_parts = set(args.scheme.split(','))
    schemes = list(map(lambda x: Scheme(x), arg_parts))

    ## Parse anonymity level
    arg_parts = set(args.anonymity_level.split(','))
    anonymity_levels = list(map(lambda x: AnonymityLevel(x), arg_parts))

    # Fetch proxies
    api = ProxyScrape()
    pset = api.fetch_proxyset(count, schemes=schemes, anonymity_levels=anonymity_levels, max_timeout=max_timeout)

    # Output proxies
    available_outformats[out_format](pset)