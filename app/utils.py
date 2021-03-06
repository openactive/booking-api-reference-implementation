from flask import request, Response
from functools import wraps
from datetime import datetime
from datetime import timedelta

import json

import constants
import errors
import models

import logging


def json_response(json_data, created=False, created_key=None, error=False):

    # remove the non-Open Active properties from the returns if they are present
    # these properties are only on Event to allow for relations between Events and Orders to be persisted locally
    if 'orderLeases' in json_data:
        del json_data['orderLeases']
    if 'completedOrders' in json_data:
        del json_data['completedOrders']

    data = json.dumps(json_data)
    data = data.replace('$HOST$', request.host_url[0:len(request.host_url) - 1])
    data = data.replace('$VERSION$', constants.API['version'])

    if error:
        response = Response(data, json_data['status'])
    else:
        if created:
            response = Response(data, 201)
            response.headers['Location'] = created_key
        else:
            response = Response(data)
    response.headers['Content-Type'] = 'application/vnd.openactive.v{version}+json'.format(
        version=constants.API['version'])
    return response


def error_response(error_condition):
    data = errors.ERRORS[error_condition]
    data['instance'] = request.path
    data['method'] = request.method
    return json_response(data, error=True)


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


def request_variables(params):
    variables = {}
    erroring_params = []
    error = False
    if request.method == "GET":
        for param in params:
            if request.args.get(param) is not None:
                if len(request.args.get(param)) != 0:
                    variables[param] = request.args.get(param)
                else:
                    erroring_params.append(param)
            else:
                erroring_params.append(param)
    else:
        if 'vnd.openactive' in request.headers['Accept']:
            request_body = request.data
            if len(request_body) > 0:
                try:
                    json_request_body = json.loads(request_body)
                except:
                    return None, params, 'not_valid_json'
            else:
                return None, params, 'no_data_supplied'
        else:
            json_request_body = request.get_json()
        for param in params:
            if param in json_request_body:
                variables[param] = json_request_body[param]
            else:
                erroring_params.append(param)
    return variables, erroring_params, error


def get_identifier(url):
    return url.rsplit('/', 1)[1]


def from_datestring(datestring):
    return datetime.strptime(datestring, "%Y-%m-%dT%H:%M:%SZ")

def is_date_in_past(this_datetime):
    if this_datetime >= datetime.now():
        return False
    else:
        return True

def add_time(this_datetime, interval, interval_type):
    if interval_type == 'M':
        return this_datetime + timedelta(minutes=interval)
    elif interval_type == 'W':
        return this_datetime + timedelta(weeks=interval)
    elif interval_type == 'D':
        return this_datetime + timedelta(days=interval)
    elif interval_type == 'H':
        return this_datetime + timedelta(hours=interval)

def clean_expired_leases(event_id):
    event_data, error = models.Event(event_id).get()
    expired_leases = []
    for lease in event_data['orderLeases']:
        logging.warn(event_data['orderLeases'][lease])
        if is_date_in_past(from_datestring(event_data['orderLeases'][lease]['leaseExpiresAt'])):
            expired_leases.append(lease)
            event_data['remainingAttendeeCapacity'] = event_data['remainingAttendeeCapacity'] + event_data['orderLeases'][lease]['places']
    if len(expired_leases) > 0:
        for lease in expired_leases:
            del event_data['orderLeases'][lease]

    event = models.Event(event_id)
    event.update(event_data)
    pass
