"""Application utility functions."""

import json
import flask
import functools
import datetime


class ADict(dict):
    """
    A dictionary with attribute-style access.
    It maps attribute access to the real dictionary.
    """
    def __init__(self, *args, **kwargs):
        super(ADict, self).__init__(*args, **kwargs)

    def _attrib(_base, _super):
        def wrapper(self, attr, *args, **kwargs):
                if attr.startswith('_'):
                    return _base(self, attr, *args, **kwargs)
                else:
                    try:
                        return _super(self, attr, *args, **kwargs)
                    except KeyError as e:
                        raise AttributeError(e)
        return wrapper

    __getattr__ = _attrib(dict.__getattribute__, dict.__getitem__)
    __setattr__ = _attrib(dict.__setattr__, dict.__setitem__)
    __delattr__ = _attrib(dict.__delattr__, dict.__delitem__)

    def copy(self):
        """Return copy of the instance."""
        return self.__class__(self)


class DateTimeEncoder(json.JSONEncoder):
    """Add extra ability to encode python datetime.datetime objects."""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            encoded_object = str(obj)
        else:
            encoded_object = json.JSONEncoder.default(self, obj)
        return encoded_object


def jsonify(func):
    """
    Replacement for built-in flask `jsonify` method.

    Allow return list-like JSON objects.
    Built-in `jsonify` disallows that.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return flask.Response(json.dumps(result, cls=DateTimeEncoder),
                              status=200, mimetype="application/json")
    return wrapper

