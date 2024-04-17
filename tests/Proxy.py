import unittest
from proxycycle.Proxy import Proxy


class TestProxy(unittest.TestCase):
    def setUp(self) -> None:
        self.proxies = [
            Proxy(host="127.0.0.1", port=8080),
            Proxy(host="127.0.0.0", port=8888)
        ]


    def test_repr(self):
        self.assertEqual(self.proxies[0], eval(repr(self.proxies[0])), "proxy != eval(repr(proxy))???")
    
    def test_equality(self):
        self.assertEqual(self.proxies[0], self.proxies[0], "proxy != proxy???")
        self.assertNotEqual(self.proxies[0], self.proxies[1], "proxy == other_proxy???")
    
    def test_hash(self):
        self.assertEqual(hash(self.proxies[0]), hash(self.proxies[0]), "hash(proxy) != hash(proxy)?????")
        self.assertNotEqual(hash(self.proxies[0]), hash(self.proxies[1]), "hash(proxy) != hash(other_proxy)?????")




if __name__ == "__main__":
    unittest.main(verbosity=3)