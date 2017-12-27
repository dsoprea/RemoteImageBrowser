import os
import unittest
import shutil
import json

import rib.config.directory_config
import rib.directory
import rib.test_support

_PLACEHOLDER_FILEPATH = \
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'rib', 'resources', 'directory_placeholder.png'))

_TEST_IMAGE_FILEPATH = \
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets', 'childpath', 'gorillababy.jpg'))


class TestDirectory(unittest.TestCase):
    def test_get_image_filepath__placeholder__empty_path(self):
        # Use the placeholder when there are no child entries.

        with rib.test_support.temp_path() as path:
            d = rib.directory.Directory()
            filepath = d.get_image_filepath(path)

            self.assertEquals(
                os.path.abspath(filepath),
                os.path.abspath(_PLACEHOLDER_FILEPATH))

    def test_get_image_filepath__placeholder__only_directories_in_path(self):
        # Use the placeholder even if there are subdirectories with images.

        with rib.test_support.temp_path() as path:
            os.mkdir('subpath')

            shutil.copyfile(
                _TEST_IMAGE_FILEPATH,
                os.path.join(path, 'subpath', 'image.jpg'))

            d = rib.directory.Directory()
            filepath = d.get_image_filepath(path)

            self.assertEquals(
                os.path.abspath(filepath),
                os.path.abspath(_PLACEHOLDER_FILEPATH))

    def test_get_image_filepath__first_found_image(self):
        with rib.test_support.temp_path() as path:
            shutil.copyfile(
                _TEST_IMAGE_FILEPATH,
                'image.jpg')

            d = rib.directory.Directory()
            filepath = d.get_image_filepath(path)

            self.assertEquals(
                os.path.abspath(filepath),
                os.path.abspath('image.jpg'))

    def test_get_image_filepath__default_directory_image(self):
        with rib.test_support.temp_path() as path:
            shutil.copyfile(
                _TEST_IMAGE_FILEPATH,
                '.directory.jpg')

            d = rib.directory.Directory()
            filepath = d.get_image_filepath(path)

            self.assertEquals(
                os.path.abspath(filepath),
                os.path.abspath('.directory.jpg'))

    def test_get_image_filepath__configured_directory_image(self):
        with rib.test_support.temp_path() as path:
            shutil.copyfile(
                _TEST_IMAGE_FILEPATH,
                'image.jpg')

            config = {
                'directory_thumbnail_filename': 'image.jpg',
            }

            with open(rib.config.directory_config.CONFIG_FILENAME, 'w') as f:
                json.dump(config, f)

            d = rib.directory.Directory()
            filepath = d.get_image_filepath(path)

            self.assertEquals(
                os.path.abspath(filepath),
                os.path.abspath('image.jpg'))
