import flask
import os
import logging

import gi
gi.require_version('GnomeDesktop', '3.0')

import gi.repository
import gi.repository.Gio
import gi.repository.GnomeDesktop

import rib.config
import rib.app
import rib.directory
import rib.exception
import rib.thumbnail.gnome
import rib.utility

_LOGGER = logging.getLogger(__name__)

@rib.app.APP.route("/api/thumbnail/download", methods=['GET'])
def api_thumbnail_download_get():
    """Return either a thumbnail for the given file or a thumbnail for the
    given path.
    """

    rel_filepath = flask.request.args.get('filepath', '')

    if rel_filepath[0] == '/':
        raise \
            rib.exception.HttpError(
                "File-path must be relative: [{}]".format(
                path))

    u = rib.utility.Utility()
    image_root_path = u.get_image_root()

    filepath = image_root_path + '/' + rel_filepath

    if os.path.exists(filepath) is False:
        raise \
            rib.exception.HttpFilesystemSubjectDoesNotExistError(
                "Filepath does not exist in image-root: [{}]->[{}]".format(
                rel_filepath, filepath))

    if os.path.isdir(filepath):
        d = rib.directory.Directory()
        directory_image_filepath = d.get_image_filepath(filepath)

        _LOGGER.debug("Getting thumbnail for path: [{}] -> [{}]".format(
                      filepath, directory_image_filepath))

        filepath = directory_image_filepath

# TODO(dustin): Make the thumbnail system pluggable for systems that don't have or don't want to use Gnome.

    g = rib.thumbnail.gnome.GnomeThumbnailer()

    try:
        thumbnail_filepath, mimetype = g.generate(filepath)
    except rib.thumbnail.gnome.ThumbnailNotSupportedError:
        thumbnail_filepath = \
            rib.config.THUMBNAIL_PLACEHOLDER_FILEPATH

        mimetype = \
            rib.config.THUMBNAIL_PLACEHOLDER_MIMETYPE

    return \
        flask.send_file(
            thumbnail_filepath,
            mimetype=mimetype)
