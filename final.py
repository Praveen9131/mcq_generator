from flask import Flask, request, jsonify
import json
import asyncio
from m import generate_quiz
from c import generate_quizc
from fill import generate_quiz1
from match import generate
from images import generate_content_internal  # Import the function from images.py

app = Flask(__name__)

@app.route('/generate_quiz')
def generate_quiz_route():
    number = request.args.get('number', default=1, type=int)
    subject = request.args.get('subject', default='general knowledge', type=str)
    tone = request.args.get('tone', default='simple', type=str)
    quiz_type = request.args.get('type', default=100, type=int)

    if quiz_type == 100:
        response = generate_quiz(number, subject, tone)  # simple mcq type
    elif quiz_type == 200:
        response = generate_quizc(number, subject, tone)  # simple checkbox type
    elif quiz_type == 300:
        response = generate_quiz1(number, subject, tone)  # fill in the blanks
    elif quiz_type == 400:
        response = generate(number, subject, tone)  # Match the sequence
    elif quiz_type == 500:
        response = asyncio.run(generate_content_internal(subject, number))  # Calls the function to handle content generation
    else:
        response = {"error": "Invalid quiz type"}

    return json.dumps(response)

if __name__ == '__main__':
    app.run(debug=True)
