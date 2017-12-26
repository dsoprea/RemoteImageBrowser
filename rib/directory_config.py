import os
import logging
import json

import rib.config.directory_config

_LOGGER = logging.getLogger(__name__)


class DirectoryConfig(object):
    def __init__(self, path):
        config_filepath = \
            os.path.join(path, rib.config.directory_config.CONFIG_FILENAME)

        try:
            with open(config_filepath) as f:
                self.__config = json.load(f)
        except IOError:
            self.__config = {}

    @property
    def directory_thumbnail_filename(self):
        return self.__config.get('directory_thumbnail_filename')
