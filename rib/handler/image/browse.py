import flask
import os
import collections
import math
import datetime

import rib.config
import rib.app
import rib.exception
import rib.filter
import rib.utility

_ENTRY = \
    collections.namedtuple(
        '_ENTRY', [
            'filename',
            'rel_filepath',
            'mtime_phrase',
            'size_phrase',
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
    u = rib.utility.Utility()

    len_ = len(image_root_path)
    for filename in children:
        filepath = os.path.join(path, filename)

        if f.include(filepath) is False:
            continue

        rel_filepath = filepath[len_ + 1:]

        s = os.stat(filepath)
        mtime_dt = datetime.datetime.fromtimestamp(s.st_mtime)

        if os.path.isdir(filepath) is True:
            e = _ENTRY(
                    rel_filepath=rel_filepath,
                    filename=filename,
                    mtime_phrase=mtime_dt.strftime(rib.config.LONG_TIMESTAMP_FORMAT),
                    size_phrase=None)

            directories.append(e)
        else:
            try:
                u.detect_image(filepath)
            except rib.utility.FileNotAnImageError:
                continue

            size_phrase = \
                '{:.1f}'.format(float(s.st_size) / 1024.0 / 1024.0)

            e = _ENTRY(
                    rel_filepath=rel_filepath,
                    filename=filename,
                    mtime_phrase=mtime_dt.strftime(rib.config.LONG_TIMESTAMP_FORMAT),
                    size_phrase=size_phrase)

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
