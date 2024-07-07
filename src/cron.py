# import serverless_wsgi
# from .services import PreInvestment
# from flask import Flask, jsonify, make_response, request


# app = Flask(__name__)


def handler(event, context):
    print("start cron job")
    print(f"event: {event}")
    print(f"context: {context}")
    return
