import urllib

import rib.app
import rib.compat

@rib.app.APP.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()

    s = s.encode('utf8')
    s = rib.compat.escape_url(s)

    return s

