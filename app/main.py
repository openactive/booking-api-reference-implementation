from flask import Flask

import utils

import logging

app = Flask(__name__)


@app.route("/")
@utils.requires_auth
def index():
    data = utils.render_json('index.json')
    return utils.json_response(data)


@app.route("/api/rdpe")
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
def order():
    variables = {
        'order': True
    }
    data = utils.render_json('fragments/linked.json', variables)
    return utils.json_response(data)


### HANDLING ERRORS ###



@app.route("/", methods=["POST","PUT","PATCH","DELETE"])
@utils.requires_auth
def index_error():
    return utils.error_response("method_not_allowed")


@app.route("/api/rdpe", methods=["POST","PUT","PATCH","DELETE"])
@utils.requires_auth
def feed_error():
    return utils.error_response("method_not_allowed")


@app.route("/api/orders", methods=["GET","PUT","PATCH","DELETE"])
@utils.requires_auth
def order_error():
    return utils.error_response("method_not_allowed")


@app.route("/<path:path>")
@utils.requires_auth
def default(path):
    return utils.error_response("not_found")
