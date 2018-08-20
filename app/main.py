from flask import Flask
import uuid

import utils
import models

import logging

app = Flask(__name__)


@app.route("/", methods=["GET"])
@utils.requires_auth
def index():
    data = utils.render_json('index.json')
    return utils.json_response(data)


@app.route("/api/rpde", methods=["GET"])
@utils.requires_auth
def feed():
    variables = {
        'next': 'blah',
        'items': []
    }
    data = utils.render_json('feed.json', variables)
    return utils.json_response(data)


@app.route("/api/orders", methods=["POST"])
@utils.requires_auth
def create_order():
    params = ['product',    'orderedItem','customer','broker']
    variables, erroring_params = utils.request_variables(params)
    if len(erroring_params) > 0:
        return utils.error_response("method_not_allowed")
    else:
        logging.warn(variables)
        order_id = str(uuid.uuid4())
        order = models.Order(order_id)
        order.create(variables)
        return utils.json_response(order.as_json_ld(), created=True, created_key=order.as_json_ld()['id'].replace('$HOST$', ''))


@app.route("/orders/<order_id>", methods=["GET"])
@app.route("/api/orders/<order_id>", methods=["GET"])
@utils.requires_auth
def get_order(order_id):
    order = models.Order(order_id)
    order.get()
    return utils.json_response(order.as_json_ld())


@app.route("/api/orders/<order_id>", methods=["PATCH"])
@utils.requires_auth
def update_order(order_id):
    order = models.Order(order_id)
    order.update({})
    return utils.json_response(order.as_json_ld())


@app.route("/api/orders/<order_id>", methods=["DELETE"])
@utils.requires_auth
def delete_order(order_id):
    order = models.Order(order_id)
    order.delete()
    return utils.json_response(order.as_json_ld())


### HANDLING ERRORS ###

# handling the disallowed verbs for the index route
@app.route("/", methods=["POST","PUT","PATCH","DELETE"])
@utils.requires_auth
def index_error():
    return utils.error_response("method_not_allowed")


# handling the disallowed verbs for the rdpe route
@app.route("/api/rpde", methods=["POST","PUT","PATCH","DELETE"])
@utils.requires_auth
def feed_error():
    return utils.error_response("method_not_allowed")


# handling the disallowed verbs for the orders collection route
@app.route("/api/orders", methods=["GET","PUT","PATCH","DELETE"])
@utils.requires_auth
def create_order_error():
    return utils.error_response("method_not_allowed")


# handling the disallowed verbs for the orders item route
@app.route("/api/orders/<order_id>", methods=["POST","PUT"])
@utils.requires_auth
def order_error(order_id):
    return utils.error_response("method_not_allowed")


# default error handling for 404, route not found
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
@utils.requires_auth
def default(path):
    return utils.error_response("not_found")
