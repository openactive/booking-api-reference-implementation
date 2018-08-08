from flask import Flask

import utils

import logging

app = Flask(__name__)


@app.route("/")
@utils.requires_auth
def hello():
    return utils.json_response({'message': 'hello world'})


@app.route("/<path:path>")
@utils.requires_auth
def default(path):
    return utils.error_response("not_found")
