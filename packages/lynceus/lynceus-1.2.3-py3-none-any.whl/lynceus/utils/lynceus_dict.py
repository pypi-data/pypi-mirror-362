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

    @staticmethod
    def _do_to_lynceus_dict(obj, *, max_depth: int, depth: int = 0):
        if depth >= max_depth:
            return obj

        if isinstance(obj, dict):
            return LynceusDict({k: LynceusDict._do_to_lynceus_dict(v, max_depth=max_depth, depth=depth + 1) for k, v in obj.items()})

        if hasattr(obj, '__dict__'):
            return LynceusDict({k: LynceusDict._do_to_lynceus_dict(v, max_depth=max_depth, depth=depth + 1) for k, v in obj.__dict__.items()})

        if isinstance(obj, list):
            return [LynceusDict._do_to_lynceus_dict(elem, max_depth=max_depth, depth=depth + 1) for elem in obj]

        return obj

    @staticmethod
    def to_lynceus_dict(obj, *, max_depth: int = 4):
        return LynceusDict._do_to_lynceus_dict(obj, max_depth=max_depth)
