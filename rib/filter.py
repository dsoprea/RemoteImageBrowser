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

    def _include_path(self, path):
        name = os.path.basename(path)

        if self._include_paths:
            for filespec in self._include_paths:
                if fnmatch.fnmatch(name, filespec) is True:
                    return True

            return False

        # If there were exclude paths, the default policy is to include.
        if self._exclude_paths:
            for filespec in self._exclude_paths:
                if fnmatch.fnmatch(name, filespec) is True:
                    return False

        # Triggers if no includes or excludes, or neither.
        return True

    def include(self, local_filepath):
        filename = os.path.basename(local_filepath)

        # Ignore hidden files (which implicitly ignores the pictures used for
        # directory images).
        if filename[0] == '.':
            return False

        if os.path.isdir(local_filepath) is False:
            # If there includes, the default policy is to exclude.

            parent_path = os.path.dirname(local_filepath)
            if parent_path != '' and self._include_path(parent_path) is False:
                return False

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
        else:
            # If there include paths, the default policy is to exclude.
            return self._include_path(local_filepath)
