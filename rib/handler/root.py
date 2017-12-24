import flask
import urllib.parse

import rib.app

@rib.app.APP.route("/", methods=['GET'])
def root_get():
    suffix = '?' + flask.request.query_string.decode()
    url = flask.url_for('image_browse_get') + suffix
    return flask.redirect(url, code=301)
