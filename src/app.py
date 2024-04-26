import serverless_wsgi
from flask import Flask, jsonify, make_response, request
import pdfkit
import boto3
import os
from .services import ContractUpdate
from .utils import generate_random_letter, date_string
from .services import PreInvestment


s3_client = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ID'),
    aws_secret_access_key=os.environ.get('AWS_KEY'),
    config=boto3.session.Config(signature_version='s3v4', region_name=os.environ.get('REGION'))
)
BUCKET = 'finniu-contracts'
AWS_S3 = f"https://{BUCKET}.s3.us-east-2.amazonaws.com/"
app = Flask(__name__)
LAMBDA_TASK_ROOT = os.environ.get('LAMBDA_TASK_ROOT', os.path.dirname(os.path.abspath(__file__)))

WKHTMLTOPDF_PATH = os.environ['WKHTMLPDF_PATH']
config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)


@app.route("/build-pdf", methods=['POST'])
def build_pdf():
    data = request.json
    html = data.get("html")
    options = {
        'encoding': 'UTF-8',
        'enable-local-file-access': True
    }
    pdf_value = pdfkit.from_string(html, False, options=options, configuration=config)
    uuid = data.get("uuid")
    filename = data.get("filename")
    random_str = generate_random_letter()
    filename_key = f"{date_string()}/{filename}-{uuid}-{random_str}.pdf"
    file_url = f"{AWS_S3}{filename_key}"
    s3_client.put_object(Body=pdf_value, Bucket=BUCKET, ContentType="application/pdf", Key=filename_key, ACL='public-read')
    ContractUpdate.execute(uuid, file_url)
    return jsonify(message='success', url=file_url)

@app.route("/purge-pre-investments", methods=['POST'])
def purge_pre_investments():
    list_pre_investments = PreInvestment.execute('draft', 100)
    return jsonify(message='success', data=list_pre_investments)

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)


