import unittest

import rib.test_support


class TestPing(unittest.TestCase):
    def test_get(self):
        import rib.handler.system.ping

        c = rib.test_support.get_test_client()
        r = c.get('/system/ping')

        self.assertEquals(r.status_code, 200)

        expected = """\
{}
"""

        self.assertEquals(r.data, expected)
