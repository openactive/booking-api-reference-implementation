from flask import Flask

import utils

import logging

app = Flask(__name__)


@app.route("/")
@utils.requires_auth
def hello():
    return utils.build_json_response({'message': 'hello world'})
