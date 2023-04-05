from flask import Flask, jsonify, make_response, request
import pdfkit
import boto3
import os
from .services import ContractUpdate
from .utils import generate_random_letter, date_string

s3_resource = boto3.resource('s3', aws_access_key_id=os.environ.get('AWS_ID'),
    aws_secret_access_key=os.environ.get('AWS_KEY'))

BUCKET = 'finniu-contracts'
AWS_S3 = f"https://{BUCKET}.s3.us-east-2.amazonaws.com/"
app = Flask(__name__)


@app.route("/build-pdf", methods=['POST'])
def build_pdf():
    data = request.json
    html = data.get("html")
    options = {
        'encoding': 'UTF-8',
        'enable-local-file-access': True
    }
    pdf_value = pdfkit.from_string(html, False, options=options)
    uuid = data.get("uuid")
    filename = data.get("filename")
    random_str = generate_random_letter()
    filename_key = f"{date_string()}/{filename}-{uuid}-{random_str}.pdf"
    file_url = f"{AWS_S3}{filename_key}"
    s3_resource.Bucket(BUCKET).put_object(
        Key=filename_key, Body=pdf_value, ContentType="application/pdf", ACL='public-read')
    ContractUpdate.execute(uuid, file_url)
    return jsonify(message='success', url=file_url)

