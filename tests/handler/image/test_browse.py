import os
import unittest
import HTMLParser

import rib.test_support


class TestParser(HTMLParser.HTMLParser):
    def __init__(self, *args, **kwargs):
        self.__images = []

        HTMLParser.HTMLParser.__init__(self, *args, **kwargs)

    def handle_starttag(self, tag, attrs):
        if tag != 'img':
            return

        self.__images.append(dict(attrs)['src'])

    @property
    def images(self):
        return self.__images


class TestBrowse(unittest.TestCase):
    def __stage(self, path):
        with open(os.path.join(path, 'image1.jpg'), 'w'):
            pass

        with open(os.path.join(path, 'image2.jpg'), 'w'):
            pass

        os.mkdir(os.path.join(path, 'subdir'))

        with open(os.path.join(path, 'subdir', 'image3.jpg'), 'w'):
            pass

    def test_get__root(self):
        import rib.handler.image.browse

        with rib.test_support.temp_path() as path:
            self.__stage(path)

            with rib.test_support.environment(
                    IMAGE_ROOT_PATH=path):
                c = rib.test_support.get_test_client()
                r = c.get('/image/browse')

                self.assertEquals(r.status_code, 200)

                p = TestParser()
                p.feed(r.data)

                expected = [
                    '/api/thumbnail/download?filepath=subdir',
                    '/api/thumbnail/download?filepath=image1.jpg',
                    '/api/thumbnail/download?filepath=image2.jpg',
                ]

                self.assertEquals(p.images, expected)

    def test_get__subdirectory(self):
        import rib.handler.image.browse

        with rib.test_support.temp_path() as path:
            self.__stage(path)

            with rib.test_support.environment(
                    IMAGE_ROOT_PATH=path):
                c = rib.test_support.get_test_client()
                r = c.get('/image/browse?path=subdir')

                self.assertEquals(r.status_code, 200)

                p = TestParser()
                p.feed(r.data)

                expected = [
                    '/api/thumbnail/download?filepath=subdir%2Fimage3.jpg',
                ]

                self.assertEquals(p.images, expected)
