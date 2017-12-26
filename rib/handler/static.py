import flask
import urllib.parse

import rib.app

# NOTE: We tried "/static" and Flask/Werkzeug wouldn't cooperate at all.
#
# REF: https://stackoverflow.com/questions/17135006/url-routing-conflicts-for-static-files-in-flask-dev-server
@rib.app.APP.route("/s/<path:rel_filepath>", methods=['GET'])
def static_static_get(rel_filepath):
    return flask.send_from_directory('rib/resources/static', rel_filepath)
