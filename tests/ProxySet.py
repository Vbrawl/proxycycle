import unittest
from proxycycle.ProxySet import ProxySet
from proxycycle.Proxy import Proxy
from proxycycle.enums import AnonymityLevel


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
        self.assertEqual(self.psl[expected_length].anonymity_level, AnonymityLevel.Anonymous, "set_proxy didn't update existing entry")
    
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
    
    # TODO: Add test for "cycle" method.

if __name__ == "__main__":
    unittest.main(verbosity=3)