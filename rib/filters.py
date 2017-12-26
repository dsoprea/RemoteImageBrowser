"""Additional Jinja filters."""

import urllib

import rib.app
import rib.utility

@rib.app.APP.template_filter('urlencode')
def urlencode_filter(s):
    u = rib.utility.Utility()
    return u.urlencode_filter(s)
