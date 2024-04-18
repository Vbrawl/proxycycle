import unittest
from proxycycle.Proxy import Proxy
from proxycycle.enums.scheme import Scheme


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

    def test_string_functions(self):
        p1string = "http://127.0.0.1:8080"
        p1 = Proxy("127.0.0.1", 8080, Scheme.HTTP)
        p2string = "socks4://127.0.0.1:8080"
        p2 = Proxy("127.0.0.1", 8080, Scheme.SOCKS4)
        p3string = "127.0.0.1:8080"
        p3 = Proxy("127.0.0.1", 8080)

        self.assertEqual(Proxy.fromString(p1string), p1, "fromString didn't return a correct object")
        self.assertEqual(Proxy.fromString(p2string), p2, "fromString didn't return a correct object")
        self.assertEqual(Proxy.fromString(p3string), p3, "fromString didn't return a correct object")

        self.assertEqual(p1.toString(), p1string, "toString didn't return a correct string representation")
        self.assertEqual(p2.toString(), p2string, "toString didn't return a correct string representation")
        self.assertEqual(p3.toString(), p3string, "toString didn't return a correct string representation")

        self.assertEqual(Proxy.fromString(p1.toString()), p1, "fromString(toString()) didn't return a correct copy of the object")
        self.assertEqual(Proxy.fromString(p2.toString()), p2, "fromString(toString()) didn't return a correct copy of the object")
        self.assertEqual(Proxy.fromString(p3.toString()), p3, "fromString(toString()) didn't return a correct copy of the object")



if __name__ == "__main__":
    unittest.main(verbosity=3)