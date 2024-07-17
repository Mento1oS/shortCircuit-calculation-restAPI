import unittest
from xml.dom import minidom

from ShortCircuitCalculator import get_current

xml_file = open("input.xml", "r").read()

doc = minidom.parseString(xml_file)


class TestCurrent(unittest.TestCase):

    def test_s1(self):
        self.assertEqual(get_current(doc)[0], 0.239)

    def test_t1(self):
        self.assertEqual(get_current(doc)[1], 2.639)

    def test_w1(self):
        self.assertEqual(get_current(doc)[2], 0.589)


if __name__ == '__main__':
    unittest.main()
