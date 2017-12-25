import flask
import os
import collections

import rib.app
import rib.exception
import rib.filter

_ENTRY = \
    collections.namedtuple(
        '_ENTRY', [
            'filename',
            'rel_filepath',
        ])

def _get_image_root():
    return os.environ['IMAGE_ROOT']

@rib.app.APP.route("/image/browse", methods=['GET'])
def image_browse_get():
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

        rel_filepath = filepath[len_ + 1:]

        e = _ENTRY(
                rel_filepath=rel_filepath,
                filename=filename)

        if os.path.isdir(filepath) is True:
            directories.append(e)
        else:
            files.append(e)

    context = {
        'rel_path': rel_path,
        'files': files,
        'directories': directories,
    }

    content = \
        flask.render_template(
            'image/browse.html',
            **context)

    response = flask.make_response(content)
    response.headers['Content-Type'] = 'text/html'

    return response
