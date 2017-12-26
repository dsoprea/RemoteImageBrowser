import urllib

import rib.app

@rib.app.APP.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()

    s = s.encode('utf8')
    s = urllib.quote_plus(s)

    return s

