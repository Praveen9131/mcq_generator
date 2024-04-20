from flask import Flask, request
import json
from m import generate_quiz
from c import generate_quizc
from fill import generate_quiz1

app = Flask(__name__)

@app.route('/generate_quiz')
def generate_quiz_route():
    number = request.args.get('number', default=1, type=int)
    subject = request.args.get('subject', default='general knowledge', type=str)
    tone = request.args.get('tone', default='simple', type=str)
    quiz_type = request.args.get('type', default=100, type=int)

    if quiz_type == 100:
        response = generate_quiz(number, subject, tone)
    elif quiz_type == 200:
        response = generate_quizc(number, subject, tone)
    elif quiz_type == 300:
        response = generate_quiz1(number,subject,tone)
    
    else:
        response = {"error": "Invalid quiz type"}

    return json.dumps(response)

if __name__ == '__main__':
    app.run(debug=True)
