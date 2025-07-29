import unittest
from routerhk import RouterHK

class TestHkClient(unittest.TestCase):
    def setUp(self):
        self.client = RouterHK()

    def test_get_ip(self):
        self.client.ip_address = None
        ip = self.client.get_ip()
        self.assertIsNotNone(ip)

if __name__ == '__main__':
    unittest.main()
