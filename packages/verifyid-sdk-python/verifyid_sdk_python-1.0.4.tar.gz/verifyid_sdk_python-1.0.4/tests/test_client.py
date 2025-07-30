import unittest
from verifyid import VerifyID

class TestVerifyID(unittest.TestCase):
    def test_init(self):
        sdk = VerifyID("dummy-key")
        self.assertIsInstance(sdk, VerifyID)

if __name__ == "__main__":
    unittest.main()
