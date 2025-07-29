import unittest

from jbussdieker.app import factory


class TestFactory(unittest.TestCase):
    def test_version(self):
        app = factory.create_app()
        self.assertTrue(app)


if __name__ == "__main__":
    unittest.main()
