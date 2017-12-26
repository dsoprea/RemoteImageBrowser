import unittest

import rib.utility
import rib.test_support


class TestUtility(unittest.TestCase):
    def test_detect_image__jpeg(self):
        u = rib.utility.Utility()
        mimetype = u.detect_image('a.jpg')

        self.assertEquals(mimetype, 'image/jpeg')

    def test_detect_image__png(self):
        u = rib.utility.Utility()
        mimetype = u.detect_image('a.png')

        self.assertEquals(mimetype, 'image/png')

    def test_detect_image__bmp(self):
        u = rib.utility.Utility()
        mimetype = u.detect_image('a.bmp')

        self.assertEquals(mimetype, 'image/bmp')

    def test_get_image_root__no_escapes(self):
        with rib.test_support.environment(
                IMAGE_ROOT='image/root/'):
            u = rib.utility.Utility()
            path = u.get_image_root()

            self.assertEquals(path, 'image/root')

    def test_urlencode_filter__with_escapes(self):
        u = rib.utility.Utility()

        escaped = u.urlencode_filter('a b c')
        self.assertEquals(escaped, 'a+b+c')

        escaped = u.urlencode_filter('a+b+c')
        self.assertEquals(escaped, 'a%2Bb%2Bc')
