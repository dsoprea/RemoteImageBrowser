import os
import logging
import fnmatch

_LOGGER = logging.getLogger(__name__)


class FileNotAnImageError(Exception):
    pass


class Utility(object):
    def detect_image(self, filepath):
        filename = os.path.basename(filepath)
        filename = filename.lower()

        if fnmatch.fnmatch(filename, '*.jpg') is True:
            return 'image/jpeg'
        elif fnmatch.fnmatch(filename, '*.png') is True:
            return 'image/png'
        elif fnmatch.fnmatch(filename, '*.bmp') is True:
            return 'image/bmp'

        raise FileNotAnImageError(filepath)

    def get_image_root(self):
        return os.environ['IMAGE_ROOT'].rstrip('/')

