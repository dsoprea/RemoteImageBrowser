import flask

import rib.app

@rib.app.APP.route("/system/ping", methods=['GET'])
def system_ping_get():
    result = {}

    encoded = flask.jsonify(result)
    return encoded
