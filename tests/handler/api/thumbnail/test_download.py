import os
import unittest
import io

import PIL.Image

import rib.test_support

_ASSETS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets'))


class TestDownload(unittest.TestCase):
    def test_get__gnome(self):
        try:
            import gi
        except ImportError:
            is_loaded = False
        else:
            is_loaded = True

        if is_loaded is False:
            raise unittest.SkipTest("Gnome not available.")

        import rib.handler.api.thumbnail.download

        with rib.test_support.environment(
                IMAGE_ROOT_PATH=_ASSETS_PATH,
                THUMBNAILER_CLASS='rib.thumbnail.gnome.GnomeThumbnailer',
                DO_RETURN_THUMBNAILER_NAME='1'):

            c = rib.test_support.get_test_client()
            r = c.get('/api/thumbnail/download?filepath=childpath/gorillababy.jpg')

            self.assertEquals(r.status_code, 200)
            self.assertEquals(r.headers['X-THUMBNAILER'], 'GnomeThumbnailer')

            s = io.BytesIO(r.data)
            im = PIL.Image.open(s)
            self.assertTrue(im.size[0] <= 128)
            self.assertTrue(im.size[1] <= 128)

    def test_get__pil(self):
        import rib.handler.api.thumbnail.download

        with rib.test_support.temp_path() as path:
            with rib.test_support.environment(
                    IMAGE_ROOT_PATH=_ASSETS_PATH,
                    THUMBNAIL_ROOT_PATH=path,
                    THUMBNAILER_CLASS='rib.thumbnail.pil.PilThumbnailer',
                    DO_RETURN_THUMBNAILER_NAME='1'):

                c = rib.test_support.get_test_client()
                r = c.get('/api/thumbnail/download?filepath=childpath/gorillababy.jpg')

                self.assertEquals(r.status_code, 200)
                self.assertEquals(r.headers['X-THUMBNAILER'], 'PilThumbnailer')

                s = io.BytesIO(r.data)
                im = PIL.Image.open(s)
                self.assertTrue(im.size[0] <= 128)
                self.assertTrue(im.size[1] <= 128)
