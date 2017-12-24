import flask

import rib.config.log
rib.config.log.configure()

import rib.config.server

APP = flask.Flask(rib.config.server.WEBSERVER_NAME)
