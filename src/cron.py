import serverless_wsgi
from .services import PreInvestment
from flask import Flask, jsonify, make_response, request


app = Flask(__name__)


def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)



