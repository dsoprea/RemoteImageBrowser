
import flask

import rib.app
import rib.exception

@rib.app.APP.errorhandler(rib.exception.HttpError)
def handle_error(error):
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    response.status = error.status_line

    return response
