from flask import Flask, request, redirect, url_for, render_template, jsonify
from google.cloud import documentai_v1beta3, storage
from google.cloud import documentai
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

storage_client = storage.Client()
bucket_name = 'aws_invoice_uploads'
bucket = storage_client.bucket(bucket_name)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file and file.filename.endswith('.pdf'):
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
        return 'File uploaded successfully.', 200
    else:
        return 'Invalid file format. Please upload a PDF.', 400
    





if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)



#import vertexai
#from vertexai.generative_models import GenerativeModel, SafetySetting
#project_id = 'tco-automation-430318'
#location = 'us'
#processor_id = '1646373740d5d523'

#vertexai.init(project="tco-automation-430318", location="us-central1")
#model = GenerativeModel("gemini-1.5-flash-001")

