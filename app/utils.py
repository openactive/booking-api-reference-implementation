from flask import request, Response
from functools import wraps
import json

import constants
import errors


def build_json_response(data, created=False, created_key=None, error=False):
    if error:
        response = Response(json.dumps(data), int(data['status']))
    else:
        response = Response(json.dumps(data))
    response.headers['Content-Type'] = 'application/vnd.openactive.v{version}+json'.format(
        version=constants.API['version'])
    if created:
        response.headers['Location'] = created_key
    return response


def check_auth(username, password):
    return username == constants.API['basicAuth']['username'] and password == constants.API['basicAuth']['password']


def return_error(error_condition):
    data = errors.ERRORS[error_condition]
    data['instance'] = request.path
    data['method'] = request.method
    return build_json_response(data, error=True)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return return_error('no_api_token_provided')
        return f(*args, **kwargs)
    return decorated
