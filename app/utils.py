from flask import request, Response, render_template
from functools import wraps
import json

import constants
import errors


def json_response(json_data, created=False, created_key=None, error=False):
    data = json.dumps(json_data)
    data = data.replace('$HOST$', request.host_url[0:len(request.host_url)-1])
    if error:
        response = Response(data, int(json_data['status']))
    else:
        if created:
            response = Response(data, 201)
            response.headers['Location'] = created_key
        else:
            response = Response(data)
    response.headers['Content-Type'] = 'application/vnd.openactive.v{version}+json'.format(version=constants.API['version'])
    return response


def error_response(error_condition):
    data = errors.ERRORS[error_condition]
    data['instance'] = request.path
    data['method'] = request.method
    return json_response(data, error=True)


def render_json(template_name, params={}):
    params['host'] = request.host_url
    rendered = render_template(template_name, **params)
    rendered = rendered.replace('$HOST$',params['host'])
    return json.loads(rendered)


def read_file(path, json_format=True):
    if json_format:
        file_contents = json.loads(open(path, 'r').read())
    else:
        file_contents = open(path, 'r').read()
    return file_contents


def check_auth(username, password):
    return username == constants.API['basicAuth']['username'] and password == constants.API['basicAuth']['password']


def check_api_key(_apikey):
    return _apikey == constants.API['apiKey']


def get_api_key():
    if 'x-api-key' in request.headers:
        return request.headers['x-api-key']
    else:
        return False


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        _auth = request.authorization
        _apikey = get_api_key()

        if _auth:
            _auth_check = check_auth(_auth.username, _auth.password)
        else:
            _auth_check = False

        if _apikey:
            _apikey_check = check_api_key(_apikey)
        else:
            _apikey_check = False

        if not _auth and not _apikey:
            return error_response('unauthenticated')
        else:
            if _auth:
                if not _auth_check:
                    return error_response('invalid_authorization_details')
            else:
                if not _apikey_check:
                    return error_response('invalid_api_token_provided')
        return f(*args, **kwargs)
    return decorated
