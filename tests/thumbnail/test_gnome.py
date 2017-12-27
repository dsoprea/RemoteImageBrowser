import os
import unittest

import PIL.Image

import rib.test_support

_ASSETS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))


class TestGnome(unittest.TestCase):
    def test_generate(self):
        try:
            import gi
        except ImportError:
            is_loaded = False
        else:
            is_loaded = True

        if is_loaded is False:
            raise unittest.SkipTest("Gnome not available.")

        image_filepath = \
            os.path.join(_ASSETS_PATH, 'childpath', 'gorillababy.jpg')

        import rib.thumbnail.gnome

        gt = rib.thumbnail.gnome.GnomeThumbnailer()
        thumbnail_filepath, thumbnail_mimetype = \
            gt.generate(image_filepath)

        im = PIL.Image.open(thumbnail_filepath)
        self.assertTrue(im.size[0] <= 128)
        self.assertTrue(im.size[1] <= 128)
