import os
import unittest

import PIL.Image

import rib.thumbnail.pil
import rib.test_support

_ASSETS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))


class TestPil(unittest.TestCase):
    def test_generate(self):
        with rib.test_support.temp_path() as path:
            with rib.test_support.environment(
                    THUMBNAIL_ROOT_PATH=path):
                image_filepath = \
                    os.path.join(_ASSETS_PATH, 'childpath', 'gorillababy.jpg')

                pt = rib.thumbnail.pil.PilThumbnailer()
                thumbnail_filepath, thumbnail_mimetype = \
                    pt.generate(image_filepath)

                self.assertEquals(
                    os.path.basename(thumbnail_filepath),
                    os.listdir(path)[0])

                im = PIL.Image.open(thumbnail_filepath)
                self.assertTrue(im.size[0] <= 128)
                self.assertTrue(im.size[1] <= 128)
