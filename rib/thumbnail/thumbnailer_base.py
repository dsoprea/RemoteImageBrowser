
class ThumbnailerBase(object):
    def generate(self, filepath):
        """Generate a thumbnail and return a 2-tuple of (thumbnail filepath,
        mime-type).
        """

        raise NotImplementedError()
