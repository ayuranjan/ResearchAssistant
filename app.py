from flask import Flask, request, jsonify, send_from_directory
import os
import fitz  # PyMuPDF
import boto3

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize AWS client (assuming you have set up AWS credentials)
# Note: For real usage, ensure you have the required AWS permissions and set up your environment correctly.
# Here, we will mock this for simplicity.
bedrock_client = boto3.client('bedrock-runtime', region_name='us-west-2')

@app.route('/sample')
def serve_html():
    return send_from_directory('.', 'sample_index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(message="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(message="No selected file"), 400
    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        extracted_text = extract_text_from_pdf(file_path)
        # Pass the text to Amazon Bedrock (Mocking the response here)
        citations = extract_citations(extracted_text)
        return jsonify(message="File successfully processed", citations=citations), 200
    else:
        return jsonify(message="Invalid file type"), 400

def extract_text_from_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    return text

def extract_citations(text):
    # Mocking Amazon Bedrock response
    # Normally, you would send the text to the Bedrock model and parse the response.
    response = bedrock_client.invoke_model(
        ModelId='anthropic.claude-3-sonnet-20240229-v1:0',
        ContentType='text/plain',
        Body=text
    )
    parsed_response = response['Body'].read().decode('utf-8')
    
    # Mocked citations extraction
    # print(text)
    # mock_citations = [
    #     "Research Paper 1: Title, Authors, Journal, Year",
    #     "Research Paper 2: Title, Authors, Journal, Year"
    # ]
    return parsed_response






if __name__ == '__main__':
    app.run(debug=True)
