import unittest

from pygolf.__main__ import main


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(main(), "PyGolf")
