import unittest

import rib.test_support


class TestRoot(unittest.TestCase):
    def test_get(self):
        import rib.handler.image.browse
        import rib.handler.root

        c = rib.test_support.get_test_client()
        r = c.get('/')

        self.assertEquals(r.status_code, 301)
        self.assertEquals(r.headers['Location'], 'http://localhost/image/browse')
