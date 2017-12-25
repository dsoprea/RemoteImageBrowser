import flask
import os

import rib.config.log
rib.config.log.configure()

import rib.config.server

template_path = \
    os.path.abspath(os.path.join('rib', 'resources', 'templates'))

APP = flask.Flask(
        rib.config.server.WEBSERVER_NAME,
        template_folder=template_path)
