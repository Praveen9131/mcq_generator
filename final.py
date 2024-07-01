from flask import Flask, request, jsonify
import asyncio
from m import generate_quiz
from c import generate_quizc
from fill import generate_quiz1
from match import generate
from images import generate_content_internal

app = Flask(__name__)

@app.route('/generate_quiz', methods=['GET'])
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
        # Using asyncio to call the Quart async function from Flask
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(generate_content_internal(subject, number))
    else:
        response = {"error": "Invalid quiz type"}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
