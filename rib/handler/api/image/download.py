import flask
import os
import imghdr

import rib.app
import rib.exception
import rib.utility

@rib.app.APP.route("/api/image/download/<path:rel_filepath>", methods=['GET'])
def api_image_download_get_by_route(rel_filepath):
    if rel_filepath == '':
        raise \
            rib.exception.HttpArgumentError(
                "Please provide 'filepath' argument.")

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
                "Filepath does not exist in image-root: [{}]".format(
                rel_filepath))

    mimetype = imghdr.what(filepath)

    return \
        flask.send_file(
            filepath,
            mimetype=mimetype)

