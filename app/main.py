from flask import Flask

import utils

import logging

app = Flask(__name__)


@app.route("/")
@utils.requires_auth
def index():
    variables = {
        "links": {
            "feed": "feed",
            "terms_and_conditions": "terms-and-conditions"
        }
    }
    data = utils.render_json('linked.json', variables)
    return utils.json_response(data)


@app.route("/<path:path>")
@utils.requires_auth
def default(path):
    return utils.error_response("not_found")
