import flask
import os
import imghdr

import gi
gi.require_version('GnomeDesktop', '3.0')

import gi.repository
import gi.repository.Gio
import gi.repository.GnomeDesktop

import rib.app
import rib.exception
import rib.thumbnail.gnome

def _get_image_root():
    return os.environ['IMAGE_ROOT']

@rib.app.APP.route("/api/image/download", methods=['GET'])
def api_image_download_get():
    rel_filepath = flask.request.args.get('filepath', '')

    if rel_filepath == '':
        raise \
            rib.exception.HttpArgumentError(
                "Please provide 'filepath' argument.")

    if rel_filepath[0] == '/':
        raise \
            rib.exception.HttpError(
                "File-path must be relative: [{}]".format(
                path))

    image_root_path = _get_image_root()
    filepath = image_root_path + '/' + rel_filepath

    if os.path.exists(filepath) is False:
        raise \
            rib.exception.HttpFilesystemSubjectDoesNotExistError(
                "Filepath does not exist in image-root: [{}]".format(
                rel_filepath))

    mimetype = imghdr.what(filepath)

    return \
        flask.send_file(
            filepath,
            mimetype=mimetype)
