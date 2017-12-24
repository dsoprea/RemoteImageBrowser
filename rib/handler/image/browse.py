import flask

import rib.app

@rib.app.APP.route("/image/browse", methods=['GET'])
def image_browse_get():
    rel_path = flask.request.args.get('path', '')

    result = {
        'rel_path': rel_path,
    }

    encoded = flask.jsonify(result)
    return encoded
