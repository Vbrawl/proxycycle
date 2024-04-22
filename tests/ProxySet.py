import unittest
from proxycycle.ProxySet import ProxySet
from proxycycle.Proxy import Proxy
from proxycycle.enums import AnonymityLevel
from io import StringIO


## NOTE: To ensure each test doesn't overlap with each other and ensure reliable results
# Each Proxy should have an IP and as we go down we increment the last octet.
#
# Example:
## The setup function adds an IP 127.0.0.0
## A function that needs to create a new IP will add the IP 127.0.0.1
## The next will add 127.0.0.2
## and so on...

class TestProxySet(unittest.TestCase):
    def setUp(self):
        self.fproxy = Proxy("127.0.0.0", 8080)
        self.psl = ProxySet([self.fproxy])
    
    def test_set_proxy(self):
        length = len(self.psl)
        expected_length = length + 1
        self.psl.set_proxy(Proxy("127.0.0.1", 8080))
        self.assertEqual(len(self.psl), expected_length, "set_proxy didn't add an inexistent proxy")

        self.psl.set_proxy(Proxy("127.0.0.1", 8080, anonymity_level=AnonymityLevel.Anonymous))
        self.assertEqual(self.psl[expected_length - 1].anonymity_level, AnonymityLevel.Anonymous, "set_proxy didn't update existing entry")
    
    def test_extend_with_proxysets(self):
        length = len(self.psl)
        expected_length = length + 2
        self.psl.extend_with_proxysets(ProxySet([
            Proxy("127.0.0.2", 8080),
            Proxy("127.0.0.3", 8080)
        ]), ProxySet([
            Proxy("127.0.0.2", 8080, anonymity_level=AnonymityLevel.Anonymous), # Replace anonymity_level of first added proxy
            Proxy("127.0.0.3", 8080, anonymity_level=AnonymityLevel.Anonymous)  # Replace anonymity_level of the second added proxy
        ]))
        self.assertEqual(len(self.psl), expected_length, "extend_with_proxysets didn't add new proxies")

        fprox = self.psl[length + 1]
        self.assertEqual(fprox.anonymity_level, AnonymityLevel.Anonymous, "extend_with_proxysets didn't update the proxy with the correct details")
    
    def test_getitem(self):
        self.assertEqual(self.psl[0], self.fproxy, "getitem didn't work for the first parameter")
        self.assertEqual(self.psl[-1], self.psl[len(self.psl) - 1], "getitem didn't work for negative or non-zero index")
    
    def test_len(self):
        plst = ProxySet()
        self.assertEqual(len(plst), 0, "Empty ProxySet should doesn't have length 0")
        plst.set_proxy(self.fproxy)
        self.assertEqual(len(plst), 1, "set_proxy didn't update len??")
    
    def test_iter(self):
        loop_number = 0
        for _ in self.psl:
            loop_number += 1
        self.assertNotEqual(loop_number, 0, "loop-iteration didn't work")
    
    def test_cycle(self):
        ps = ProxySet([
            Proxy("127.0.0.0", 8080)
        ])

        it = ps.cycle()
        self.assertEqual(next(it), next(it), "cycle didn't return the same object twice in a single item ProxySet")
    
    def test_fromFile(self):
        fdata = StringIO()
        fdata.writelines(map(Proxy.toString, self.psl))
        fdata.seek(0)
        psl2 = ProxySet.fromFile(fdata)

        self.assertEqual(len(self.psl), len(psl2), "fromFile didn't load all proxies")

        for i, proxy in enumerate(self.psl):
            self.assertEqual(proxy, psl2[i], "fromFile didn't return a ProxySet with the correct proxies")
    

    def test_deduplicate(self):
        proxies = ProxySet([
            Proxy("127.0.0.4", 8000),
            Proxy("127.0.0.4", 8001, anonymity_level=AnonymityLevel.Anonymous),
            Proxy("127.0.0.4", 8002, anonymity_level=AnonymityLevel.Elite),
            Proxy("127.0.0.5", 8000),
            Proxy("127.0.0.6", 8002)
        ])

        nproxies = proxies.deduplicate()

        self.assertEqual(len(nproxies), 3)

        def select_elite_anonymity(proxies:list[Proxy]):
            for i in proxies:
                if i.anonymity_level == AnonymityLevel.Elite:
                    return i
            return None
        nproxies2 = proxies.deduplicate(select_elite_anonymity)

        self.assertEqual(len(nproxies2), 1)

        def select_8002_ports(proxies:list[Proxy]):
            for i in proxies:
                if i.port == 8002:
                    return i
            return None
        nproxies3 = proxies.deduplicate(select_8002_ports)

        self.assertEqual(len(nproxies3), 2)

if __name__ == "__main__":
    unittest.main(verbosity=3)