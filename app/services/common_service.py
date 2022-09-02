from flask import jsonify


def service_handler(func):
    data, error = func
    response = data if not error else {'error': error}
    status_code = 200 if data else 404 if not error else 400
    return jsonify(response), status_code
