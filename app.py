from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Initialize the summarizer
summarizer = pipeline("summarization", model="t5-small")

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')  # Render your front-end HTML file

# Route for the summarization functionality
@app.route('/summarize', methods=['POST'])
def summarize():
    email_body = request.form.get('email_body')  # Get email text from the form
    if email_body and email_body.strip():
        summary = summarizer(email_body, max_length=50, min_length=25, do_sample=False)
        return jsonify({'summary': summary[0]['summary_text']})
    return jsonify({'error': 'Please enter some text.'})

if __name__ == '__main__':
    app.run(debug=True)
