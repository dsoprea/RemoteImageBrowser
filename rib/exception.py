class HttpError(Exception):
    status_code = 501
    status_line = 'GENERAL ERROR'

    def __init__(self, *args, **kwargs):
        super(HttpError, self).__init__(*args, **kwargs)

    def to_dict(self):
        data = {
            'message': str(self)
        }

        return data

class HttpFilesystemError(HttpError):
    status_code = 502
    status_line = 'FS GENERAL ERROR'

class HttpFilesystemSubjectDoesNotExistError(HttpFilesystemError):
    status_code = 503
    status_line = 'FS SUBJECT DOES NOT EXIST'


class ImageError(Exception):
    status_code = 504
    status_line = 'IMAGE ERROR'


class HttpArgumentError(HttpError):
    status_code = 505
    status_line = 'ARGUMENT ERROR'
