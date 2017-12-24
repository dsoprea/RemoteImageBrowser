import flask
import os

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

@rib.app.APP.route("/api/thumbnail/download", methods=['GET'])
def api_thumbnail_download_get():
    rel_filepath = flask.request.args.get('rel_filepath', '')

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

# TODO(dustin): Make the thumbnail system pluggable for systems that don't have or don't want to use Gnome.

    g = rib.thumbnail.gnome.GnomeThumbnailer()
    thumbnail_filepath, mimetype = g.generate(filepath)

    return \
        flask.send_file(
            thumbnail_filepath,
            mimetype=mimetype)
