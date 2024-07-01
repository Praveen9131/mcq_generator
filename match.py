import os
import json
from flask import Flask, request, jsonify
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
from langchain.chains import SequentialChain
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
KEY = os.getenv("OPENAI_API_KEY")

def generate (number, subject, tone):
    llm = ChatOpenAI(openai_api_key=KEY, model_name="gpt-4", temperature=0.5)
    
    # Construct the predefined text for the quiz
    predefined_text = f"Based on the fundamentals of {subject}, create a quiz that encompasses the core concepts and challenges students' understanding."
    
    # Construct the template with proper variable replacement
    TEMPLATE = f"""
    Text: {predefined_text}
    You are an expert sequence maker. Given the above text, it is your job to \
    create a quiz of {number} sequence for {subject} students in {tone} tone. 
    Make sure the questions are not repeated and check all the questions to be conforming the text as well.
    Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
    Ensure to make {number} MCQs in the format of above variable 
    , please give me in this format RESPONSE_JSON format of array and use the keywords only question, options, answer.
    Show me first question then options then answer
    Don't generate question numbers.
    "question": Match the sequence for following,
    "options": ["India", "USA", "UK", "Japan"],
    "correct": "New Delhi"
    // More questions as needed...
    """

    quiz_generation_prompt = PromptTemplate(
        input_variables=["number", "subject", "tone"],
        template=TEMPLATE
    )

    # Define the LLMChain for generating the quiz
    quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz")
    
    # Generate the quiz using the chain
    response = quiz_chain({
        "number": number,
        "subject": subject,
        "tone": tone
    })

    # Extract the quiz JSON string from the response
    quiz_json = response.get("quiz")

    # Check if quiz_json is None or empty
    if quiz_json:
        try:
            # Parse the quiz JSON string
            quiz_data = json.loads(quiz_json)
            return quiz_data
        except json.JSONDecodeError as e:
            return {"error": "Failed to parse quiz JSON"}
    else:
        return {"error": "No quiz generated"}
