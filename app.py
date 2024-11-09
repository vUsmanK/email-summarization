from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import AzureOpenAI
import os
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

endpoint = os.getenv("ENDPOINT_URL", "https://ai-mehaknauman6ai9219481888056792.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "9a38b6fa427a45eaba28ffa8bf4d88a6")

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-05-01-preview",
)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/')
def index():
    return send_from_directory('.', 'email summariser.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        email_text = data['email']
        
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are an AI that summarizes emails."},
                {"role": "user", "content": email_text}
            ],
            max_tokens=100
        )
        
        summary = response.choices[0].message['content'].strip()
        return jsonify({'summary': summary})
    except Exception as e:
        app.logger.error('Error during summarization: %s', e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)