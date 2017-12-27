import sys
import unittest

import rib.compat


class TestCompat(unittest.TestCase):
    unittest.skipIf(sys.version_info.major != 2, "Not Python 2.")
    def test_escape_url__2(self):
        escaped = rib.compat.escape_url('a+b')
        self.assertEquals(escaped, 'a%2Bb')

    unittest.skipIf(sys.version_info.major != 3, "Not Python 3.")
    def test_escape_url__3(self):
        escaped = rib.compat.escape_url('a+b')
        self.assertEquals(escaped, 'a%2Bb')
