import os
import logging

import gi
gi.require_version('GnomeDesktop', '3.0')

import gi.repository
import gi.repository.Gio
import gi.repository.GnomeDesktop

import rib.exception
import rib.thumbnail.thumbnailer_base

_LOGGER = logging.getLogger(__name__)


class ThumbnailNotSupportedError(rib.exception.ImageError):
    pass


class GnomeThumbnailer(rib.thumbnail.thumbnailer_base.ThumbnailerBase):
    def generate(self, filepath):
        mtime = os.path.getmtime(filepath)

        # Use Gio to determine the URI and mime type
        f = gi.repository.Gio.file_new_for_path(filepath)

        uri = f.get_uri()

        info = f.query_info(
                'standard::content-type',
                gi.repository.Gio.FileQueryInfoFlags.NONE,
                None)

        mimetype = info.get_content_type()

        factory = gi.repository.GnomeDesktop.DesktopThumbnailFactory()

        thumbnail_filepath = factory.lookup(uri, mtime)

        if thumbnail_filepath is None:
            can_thumbnail = factory.can_thumbnail(uri, mimetype, mtime)

# TODO(dustin): Might want to abstract this so the browse view knows which files to exclude.
            if can_thumbnail is False:
                raise \
                    ThumbnailNotSupportedError(
                        "Does not support thumbnailing: [{}]".format(filepath))

            thumbnail = factory.generate_thumbnail(uri, mimetype)

            if thumbnail is None:
                raise \
                    rib.exception.ImageError(
                        "Thumbnail generation failed: [{}]".format(filepath))

            factory.save_thumbnail(thumbnail, uri, mtime)
            thumbnail_filepath = factory.lookup(uri, mtime)

        return thumbnail_filepath, mimetype
