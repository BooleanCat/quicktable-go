from quicktable import add
from unittest import TestCase


class TestAdd(TestCase):
    def test_add(self):
        self.assertEqual(4, add(1, 3))
