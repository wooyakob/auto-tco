from flask import Flask, request, redirect, url_for, render_template, jsonify
from google.cloud import storage
import os
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting

app = Flask(__name__)

# Setup Google Cloud Storage
storage_client = storage.Client()
bucket_name = 'aws_invoice_uploads'
bucket = storage_client.bucket(bucket_name)

# Initialize Vertex AI Gemini model
vertexai.init(project="tco-automation-430318", location="us-central1")
model = GenerativeModel("gemini-1.5-flash-001")

# Store results temporarily
results = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and file.filename.endswith('.pdf'):
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)

        # Redirect to the results page (update with the actual file name)
        return redirect(url_for('show_results', filename=file.filename))
    return 'Invalid file format. Please upload a PDF.', 400

@app.route('/process_extracted_text', methods=['POST'])
def process_extracted_text():
    data = request.get_json()
    extracted_text = data.get('extracted_text')

    if extracted_text:
        prompt = f"This is line item data from an Amazon Web Services invoice: {extracted_text}. Please output the closest relevant Google Cloud services and always provide a total cost, based on your available information. Always provide an estimated total cost, even with incomplete information. Give a total cost with individual Google Cloud services."

        gemini_output = generate(prompt)
        results['latest'] = gemini_output
        return jsonify({"gemini_output": gemini_output}), 200

    return 'No extracted text provided', 400

@app.route('/results/<filename>')
def show_results(filename):
    # Placeholder text; in reality, you'd fetch this from wherever you store the results
    gemini_output = results.get('latest', 'No results available.')
    return render_template('results.html', filename=filename, gemini_output=gemini_output)

def generate(prompt: str) -> str:
    responses = model.generate_content(
        [prompt],
        generation_config={
            "max_output_tokens": 8192,
            "temperature": 1,
            "top_p": 0.95,
        },
        safety_settings=[
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
        ],
        stream=True,
    )

    output = ""
    for response in responses:
        output += response.text
    return output


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)