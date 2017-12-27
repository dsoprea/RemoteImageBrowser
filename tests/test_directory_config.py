import unittest
import json

import rib.config.directory_config
import rib.directory_config
import rib.test_support


class TestDirectoryConfig(unittest.TestCase):
    def test_directory_thumbnail_filename(self):
        with rib.test_support.temp_path() as path:
            config = {
                'directory_thumbnail_filename': 'image.jpg',
            }

            with open(rib.config.directory_config.CONFIG_FILENAME, 'w') as f:
                json.dump(config, f)

            dc = rib.directory_config.DirectoryConfig(path)
            self.assertEquals(dc.directory_thumbnail_filename, 'image.jpg')
