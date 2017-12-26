import unittest

import rib.filters
import rib.app
import rib.test_support


class TestFilters(unittest.TestCase):
    def test_urlencode_filter(self):
        # The filter is implicitly loaded by the import.

        t = rib.app.APP.jinja_env.from_string("""\
{{ "abc" | urlencode }}
""")

        self.assertEquals(t.render(), "abc")

        t = rib.app.APP.jinja_env.from_string("""\
{{ "a b c" | urlencode }}
""")

        self.assertEquals(t.render(), "a+b+c")

        t = rib.app.APP.jinja_env.from_string("""\
{{ "a+b+c" | urlencode }}
""")

        self.assertEquals(t.render(), "a%2Bb%2Bc")
