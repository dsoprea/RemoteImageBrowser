import os

IS_DEBUG = bool(int(os.environ.get('DEBUG', '0')))

LONG_TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

THUMBNAIL_PLACEHOLDER_FILEPATH = 'rib/resources/directory_placeholder.png'
THUMBNAIL_PLACEHOLDER_MIMETYPE = 'image/png'
