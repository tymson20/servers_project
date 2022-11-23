import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer, TooManyProductsFoundError

server_types = (ListServer, MapServer)


class ProductTest(unittest.TestCase):

    def test_product_has_correct_name(self):
        products = [Product("a2", 1.0), Product("Ab11", 0.0)]
        self.assertEqual(products[0].name, "a2")
        self.assertEqual(products[1].name, "Ab11")

    def test_product_has_incorrect_name(self):
        incorrect_names = ("1b", "11", "A")
        for name in incorrect_names:
            with self.assertRaises(ValueError) as context:
                product = Product(name, 0.0)

            self.assertTrue("Incorrect name of product" in str(context.exception))

    def test_products_are_equal(self):
        product1 = Product("a1", 1.2)
        product2 = Product("a1", 1.2)
        self.assertTrue(product1.__eq__(product2))


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

    def test_get_entries_returns_empty_list(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(3)
            self.assertEqual(entries, [])

    def test_get_entries_raises_TooManyProductsFoundError(self):
        products = [Product('Pa12', 1), Product('Pa234', 2), Product('Pa235', 1), Product('Pa240', 3)]
        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(TooManyProductsFoundError):
                entries = server.get_entries(2)


class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))

    def test_total_price_for_normal_execution_float(self):
        products = [Product('PP234', 6.5), Product('PP235', 10.3),Product('PP236',4.5)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(21.3, client.get_total_price(2))

    def test_total_price_returns_None(self):
        products = [Product('PP12', 1), Product('PP234', 2), Product('PP235', 1), Product('PP236', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(3))
            self.assertEqual(None, client.get_total_price(2))


if __name__ == '__main__':
    unittest.main()