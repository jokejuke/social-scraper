"""Application utility functions."""

import json
import flask
import functools


def jsonify(func):
    """
    Replacement for built-in flask `jsonify` method.

    Allow return list-like JSON objects.
    Built-in `jsonify` disallows that.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return flask.Response(json.dumps(result), status=200,
                              mimetype="application/json")
    return wrapper

