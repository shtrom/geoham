import unittest

try:
    # for Python 2.x
    from StringIO import StringIO
except ImportError:
    # for Python 3.x
    from io import StringIO
import csv

from geoham.parser import Parser


class TestParser(unittest.TestCase):

    TEST_CSV = '''Output, Input, Call, mNemonic, Location, Service Area, Latitude, Longitude, S, ERP, HASL, T/O, Sp, Tone, Notes
29.1200, 29.1200, VK2RMB, THills, Terrey Hills, Sydney 6/15, -33.692994, 151.222079, P, -, 150, -, 2MB, -, 1
29.1200, 29.1200, VK2RBH, Darlng, Mt Darling, Broken Hill, -32.022963, 141.533162, O, -, 400, -, 2DPG, -, 12'''

    def test_parse(self):
        f = StringIO(self.TEST_CSV)
        parser = Parser()

        parsed, skipped = parser.parse(f)

        self.assertIsNotNone(parsed)
        self.assertIsNone(skipped)


if __name__ == '__main__':
    unittest.main()
