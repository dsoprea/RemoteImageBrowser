import rib.app
import rib.filters

import rib.handler.error

import rib.handler.api.image.browse
import rib.handler.api.thumbnail.download
import rib.handler.api.image.download

import rib.handler.image.browse
import rib.handler.system.ping
import rib.handler.static
import rib.handler.root

# TODO(dustin): This configures to print to the console. How to use UWSGI for logging?
#
# import rib.config.log
# rib.config.log.configure()

APP = rib.app.APP
