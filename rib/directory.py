import os
import logging

import rib.config
import rib.directory_config
import rib.utility

_LOGGER = logging.getLogger(__name__)


class Directory(object):
    def get_image_filepath(self, path):
        """Return an image to represent the path with. Return None if no image
        could be determined.
        """

        thumbnail_filename = \
            rib.config.THUMBNAIL_PLACEHOLDER_FILEPATH

        db = rib.directory_config.DirectoryConfig(path)
        config_thumbnail_filename = db.directory_thumbnail_filename

        if config_thumbnail_filename is not None:
            thumbnail_filename = config_thumbnail_filename

        filepath = os.path.join(path, thumbnail_filename)

        if os.path.exists(filepath) is True:
            return filepath

        u = rib.utility.Utility()
        f = rib.filter.Filter()

        for filename in sorted(os.listdir(path)):
            filepath = os.path.join(path, filename)

            if f.include(filepath) is False:
                continue

            try:
                u.detect_image(filepath)
            except rib.utility.FileNotAnImageError:
                continue
            else:
                return filepath

        return \
            rib.config.THUMBNAIL_PLACEHOLDER_FILEPATH
