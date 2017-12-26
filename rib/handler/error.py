import logging

import flask

import rib.app
import rib.exception

_LOGGER = logging.getLogger(__name__)

@rib.app.APP.errorhandler(rib.exception.HttpError)
def handle_error(error):
    _LOGGER.error("({}) [{}] {}".format(
                  error.status_code, error.status_line, str(error)))

    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    response.status = error.status_line

    return response
