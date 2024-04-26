import serverless_wsgi
from .services import PreInvestment
from flask import Flask, jsonify, make_response, request


app = Flask(__name__)

@app.route("/purge-pre-investments", methods=['POST'])
def purge_pre_investments():
    list_pre_investments = PreInvestment.execute('draft', 100)
    return jsonify(message='success', data=list_pre_investments)
def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)



