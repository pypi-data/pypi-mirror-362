class LynceusDict(dict):
    """
    Little dict enhancement allowing [.] attribute access, in addition to usual [key] ones.
    """
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as key_error:
            raise AttributeError from key_error

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as key_error:
            raise AttributeError from key_error
