import flask
import os
import logging

import rib.config
import rib.config.handler.api.thumbnail.download
import rib.app
import rib.directory
import rib.exception
import rib.thumbnail.thumbnailer_base
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

    fq_class = \
        os.environ.get(
            'THUMBNAILER_CLASS',
            rib.config.handler.api.thumbnail.download.DEFAULT_THUMBNAILER_FQ_CLASS)

    pivot = fq_class.rindex('.')
    fq_module = fq_class[:pivot]
    class_name = fq_class[pivot + 1:]

    m = __import__(fq_module, fromlist=[class_name])
    cls = getattr(m, class_name)

    assert \
        issubclass(cls, rib.thumbnail.thumbnailer_base.ThumbnailerBase) is True, \
        "Thumbnailer does not have correct baseclass: [{}]".format(fq_class)

    t = cls()

    try:
        thumbnail_filepath, mimetype = t.generate(filepath)
    except rib.exception.ImageError:
        thumbnail_filepath = \
            rib.config.THUMBNAIL_PLACEHOLDER_FILEPATH

        mimetype = \
            rib.config.THUMBNAIL_PLACEHOLDER_MIMETYPE

    sf = flask.send_file(
            thumbnail_filepath,
            mimetype=mimetype)

    r = flask.make_response(sf)

    send_thumbnailer = \
        bool(int(os.environ.get('DO_RETURN_THUMBNAILER_NAME', '0')))

    if send_thumbnailer is True:
        r.headers['X-THUMBNAILER'] = class_name

    return r
