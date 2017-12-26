import os
import unittest

import rib.test_support
import rib.filter


class TestFilter(unittest.TestCase):
    def __stage(self, path):
        os.mkdir(os.path.join(path, 'abc'))

        with open(os.path.join(path, 'abc', 'filename1'), 'w'):
            pass

        os.mkdir(os.path.join(path, 'def'))

        with open(os.path.join(path, 'def', 'filename2'), 'w'):
            pass

    def test_include__include_path(self):
        with rib.test_support.temp_path() as path:
            self.__stage(path)

            with rib.test_support.environment(
                    INCLUDE_PATHS='abc'):
                    f = rib.filter.Filter()

                    self.assertTrue(f.include(os.path.join(path, 'abc')))
                    self.assertFalse(f.include(os.path.join(path, 'def')))
                    self.assertTrue(f.include(os.path.join(path, 'abc', 'filename1')))
                    self.assertFalse(f.include(os.path.join(path, 'def', 'filename2')))

    def test_include__exclude_path(self):
        with rib.test_support.temp_path() as path:
            self.__stage(path)

            with rib.test_support.environment(
                    EXCLUDE_PATHS='abc'):
                    f = rib.filter.Filter()

                    self.assertFalse(f.include(os.path.join(path, 'abc')))
                    self.assertTrue(f.include(os.path.join(path, 'def')))
                    self.assertFalse(f.include(os.path.join(path, 'abc', 'filename1')))
                    self.assertTrue(f.include(os.path.join(path, 'def', 'filename2')))

    def test_include__include_file(self):
        with rib.test_support.temp_path() as path:
            self.__stage(path)

            with rib.test_support.environment(
                    INCLUDE_FILES='filename1'):
                    f = rib.filter.Filter()

                    self.assertTrue(f.include(os.path.join(path, 'abc')))
                    self.assertTrue(f.include(os.path.join(path, 'def')))
                    self.assertTrue(f.include(os.path.join(path, 'abc', 'filename1')))
                    self.assertFalse(f.include(os.path.join(path, 'def', 'filename2')))


    def test_include__exclude_file(self):
        with rib.test_support.temp_path() as path:
            self.__stage(path)

            with rib.test_support.environment(
                    EXCLUDE_FILES='filename1'):
                    f = rib.filter.Filter()

                    self.assertTrue(f.include(os.path.join(path, 'abc')))
                    self.assertTrue(f.include(os.path.join(path, 'def')))
                    self.assertFalse(f.include(os.path.join(path, 'abc', 'filename1')))
                    self.assertTrue(f.include(os.path.join(path, 'def', 'filename2')))

