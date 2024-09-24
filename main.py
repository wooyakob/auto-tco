"""from flask import Flask, request, redirect, url_for, render_template, jsonify
from google.cloud import documentai_v1beta3, storage
from google.cloud import documentai
from google.api_core.client_options import ClientOptions
from typing import Optional, Sequence
import os
import json
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting, FinishReason
import vertexai.generative_models as generative_models
import re


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

        response_text = process_document(bucket_name, file.filename)

        return render_template('index.html', response_text=response_text)
    else:
        return 'Invalid file format. Please upload a PDF.', 400


#Document processing function, send to document AI custom processor from Cloud Storage Bucket

def process_document(bucket_name, object_name):
    client = documentai_v1beta3.DocumentProcessorServiceClient()

    file_path = f"/tmp/{object_name}"
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.download_to_filename(file_path)

    with open(file_path, "rb") as image:
        image_content = image.read()
    
    document = {"content": image_content, "mime_type": "application/pdf"}
    processor_name = "projects/tco-automation-430318/locations/us/processors/1646373740d5d523"
    
    request = {"name": processor_name, "document": document}
    
    try:
        result = client.process_document(request=request, timeout=3600)
        document = result.document

        #print(document)
        #print(document.entities)
        print(document.text)

        prompt_text = f"Take a deep breath and carefully review the following {document.text}, which contains detailed invoice data from Amazon Web Services, including services, usage, and associated costs.\n\nYour task is to conduct a cloud cost assessment by identifying equivalent Google Cloud Platform services that match the usage described. Using the latest pricing data available to you, provide an estimated grand total and a detailed breakdown of the GCP services, usage, and corresponding costs that make up this total.\n\nDo not include any disclaimers, assumptions, or recommendations to consult additional documentation. Simply present the estimated total and the list of equivalent services, usage, and their respective costs, without phrases like 'assuming similar usage.'"
        response_text = generate_cost_assessment(prompt_text)
        return response_text
        
    except Exception as e:
        print(f"Error processing document: {e}")
        return f"Error processing document: {e}"
    
def clean_text(text):
    # Remove #, ##, |, *, and **
    text = re.sub(r'[#|*]+', '', text)
    # Remove any remaining standalone * or ** (bold/italic markdown)
    text = re.sub(r'\*\*', '', text)
    text = re.sub(r'\*', '', text)
    return text

def generate_cost_assessment(prompt_text):
    vertexai.init(project="tco-automation-430318", location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-001")
    
    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }

    safety_settings = [
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
    ]

    responses = model.generate_content(
        [prompt_text],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    response_text = ""
    for response in responses:
        response_text += response.text


    # Clean and format the response text
    response_text = clean_text(response_text)

    return response_text


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)"""