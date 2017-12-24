import logging
import os
import fnmatch

_LOGGER = logging.getLogger(__name__)


class Filter(object):
    def __init__(self):
        include_paths_raw = os.environ.get('INCLUDE_PATHS', '')

        if include_paths_raw == '':
            self._include_paths = []
        else:
            self._include_paths = include_paths_raw.split(',')

        _LOGGER.debug("INCLUDE_PATHS = {}".format(self._include_paths))

        include_files_raw = os.environ.get('INCLUDE_FILES', '')

        if include_files_raw == '':
            self._include_files = []
        else:
            self._include_files = include_files_raw.split(',')

        _LOGGER.debug("INCLUDE_FILES = {}".format(self._include_files))

        exclude_paths_raw = os.environ.get('EXCLUDE_PATHS', '')

        if exclude_paths_raw == '':
            self._exclude_paths = []
        else:
            self._exclude_paths = exclude_paths_raw.split(',')

        _LOGGER.debug("EXCLUDE_PATHS = {}".format(self._exclude_paths))

        exclude_files_raw = os.environ.get('EXCLUDE_FILES', '')

        if exclude_files_raw == '':
            self._exclude_files = []
        else:
            self._exclude_files = exclude_files_raw.split(',')

        _LOGGER.debug("EXCLUDE_FILES = {}".format(self._exclude_files))

    def include(self, local_filepath):
        filename = os.path.basename(local_filepath)

        if os.path.isdir(local_filepath) is True:
            # If there include paths, the default policy is to exclude.

            if self._include_paths:
                for filespec in self._include_paths:
                    if fnmatch.fnmatch(filename, filespec) is True:
                        return True

                return False

            # If there were exclude paths, the default policy is to include.
            if self._exclude_paths:
                for filespec in self._exclude_paths:
                    if fnmatch.fnmatch(filename, filespec) is True:
                        return False

            # Triggers if no includes or excludes, or neither.
            return True
        else:
            # If there includes, the default policy is to exclude.

            if self._include_files:
                for filespec in self._include_files:
                    if fnmatch.fnmatch(filename, filespec) is True:
                        return True

                return False

            # If there were excludes, the default policy is to include.
            if self._exclude_files:
                for filespec in self._exclude_files:
                    if fnmatch.fnmatch(filename, filespec) is True:
                        return False

            # Triggers if no includes or excludes, or neither.
            return True
