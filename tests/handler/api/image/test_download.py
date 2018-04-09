import os
import unittest

import rib.test_support

_ASSETS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets'))


class TestDownload(unittest.TestCase):
    def test_get(self):
        import rib.handler.api.image.download

        with rib.test_support.environment(
                IMAGE_ROOT_PATH=_ASSETS_PATH):
            c = rib.test_support.get_test_client()
            r = c.get('/api/image/download/childpath/gorillababy.jpg')

            self.assertEquals(r.status_code, 200)

            with open(os.path.join(_ASSETS_PATH, 'childpath', 'gorillababy.jpg'), 'rb') as f:
                expected = f.read()

            self.assertEquals(r.data, expected)
