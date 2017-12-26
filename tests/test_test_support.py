import os
import unittest

import rib.test_support


class TestTestSupport(unittest.TestCase):
    def test_environment__noop(self):
        os.environ['TEST_VARIABLE'] = 'aa'

        with rib.test_support.environment():
            self.assertEquals(os.environ['TEST_VARIABLE'], 'aa')

    def test_environment__del(self):
        os.environ['TEST_VARIABLE'] = 'aa'

        with rib.test_support.environment(
                TEST_VARIABLE=None):
            self.assertIsNone(os.environ.get('TEST_VARIABLE'))

    def test_environment__no_sideeffects(self):
        os.environ['TEST_VARIABLE'] = 'aa'

        with rib.test_support.environment(
                TEST_VARIABLE='bb'):
            self.assertEquals(os.environ['TEST_VARIABLE'], 'bb')

        self.assertEquals(os.environ['TEST_VARIABLE'], 'aa')

    def test_environment__cleanup(self):
        with rib.test_support.environment(
                TEST_VARIABLE='cc'):
            self.assertEquals(os.environ['TEST_VARIABLE'], 'cc')

        self.assertIsNone(os.environ.get('TEST_VARIABLE'))
