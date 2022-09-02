from flask import jsonify
from functools import wraps


def service_handler():
    def decorator(service):
        @wraps(service)
        def inner(*args, **kwargs):
            data, error = service(*args, **kwargs)
            response = data if not error else {'error': error}
            status = 200 if data else 404 if not error else 400
            return jsonify(response), status
        return inner
    return decorator
