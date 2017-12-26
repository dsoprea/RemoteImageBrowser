import flask
import os
import logging.config

import rib.config.server

template_path = \
    os.path.abspath(os.path.join('rib', 'resources', 'templates'))

# Up the log-level to INFO.
logging.config.dictConfig({
    'version': 1,
    'root': {
        'level': 'INFO',
    }
})

APP = flask.Flask(
        rib.config.server.WEBSERVER_NAME,
        template_folder=template_path,
        static_url_path='/static')
