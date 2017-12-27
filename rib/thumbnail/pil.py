import os
import logging
import hashlib
import math

import PIL.Image

import rib.thumbnail.thumbnailer_base

_LOGGER = logging.getLogger(__name__)

_MAX_DIM = 128


class PilThumbnailer(rib.thumbnail.thumbnailer_base.ThumbnailerBase):
    def __init__(self):
        path = os.environ['THUMBNAIL_ROOT_PATH']

        assert \
            os.path.exists(path) is True, \
            "Thumbnail path does not exist: [{}]".format(path)

        self.__path = path

    def generate(self, filepath):
        filename = os.path.basename(filepath)
        _, extension = os.path.splitext(filename)

        thumbnail_filename = hashlib.sha1(filepath.encode('utf-8')).hexdigest() + extension
        thumbnail_filepath = os.path.join(self.__path, thumbnail_filename)

        if os.path.exists(thumbnail_filepath) is False:
            im = PIL.Image.open(filepath)
            format_ = im.format

            if im.size[0] > _MAX_DIM or im.size[1] > _MAX_DIM:
                im.thumbnail((_MAX_DIM, _MAX_DIM), PIL.Image.ANTIALIAS)
                im.save(thumbnail_filepath)
            else:
                thumbnail_filepath = filepath
        else:
            im = PIL.Image.open(thumbnail_filepath)
            format_ = im.format

        return thumbnail_filepath, PIL.Image.MIME[format_]
