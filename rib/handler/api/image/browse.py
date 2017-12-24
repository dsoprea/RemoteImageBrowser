import flask
import os

import rib.app
import rib.exception
import rib.filter

def _get_image_root():
    return os.environ['IMAGE_ROOT']

@rib.app.APP.route("/api/image/browse", methods=['GET'])
def api_image_browse_get():
    rel_path = flask.request.args.get('path', '')

    if rel_path and rel_path[0] == '/':
        raise \
            rib.exception.HttpError(
                "Path must be relative to image-root or empty: [{}]".format(
                path))

    image_root_path = _get_image_root()
    path = image_root_path

    rel_path = rel_path.rstrip('/')

    if rel_path != '':
        path = os.path.join(path, rel_path)

    if os.path.exists(path) is False:
        raise \
            rib.exception.HttpFilesystemSubjectDoesNotExistError(
                "Path does not exist in image-root: [{}]".format(rel_path))

    children = os.listdir(path)
    children = sorted(children)

    directories = []
    files = []

    f = rib.filter.Filter()

    len_ = len(image_root_path)
    for filename in children:
        filepath = os.path.join(path, filename)

        if f.include(filepath) is False:
            continue

        if os.path.isdir(filepath) is True:
            directories.append(filepath[len_ + 1:])
        else:
            files.append(filename)

    result = {
        'directories': directories,
        'files': files,
    }

    encoded = flask.jsonify(result)
    return encoded
