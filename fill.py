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

def generate_quiz1(number, subject, tone):
    llm = ChatOpenAI(openai_api_key=KEY, model_name="gpt-4", temperature=0.5)
    RESPONSE_JSON = {
    "questions": [
        {
            "statement": "Question statement here",
            "options": [
                "[].Option 1",
                "[].Option 2",
                "[].Option 3",
                "[].Option 4" "generate the []symbol for each option"
            ],
            "correct": ["Option 1", "Option 3"]  # List all correct options
        }
        # More questions as needed...
    ]
}
    # Construct the predefined text for the quiz
    predefined_text = f"Based on the fundamentals of {subject}, create a quiz that encompasses the core concepts and challenges students' understanding."
    
    # Construct the template without using RESPONSE_JSON directly unless it's a variable you pass to LLMChain
    TEMPLATE = f"""
    Text: {predefined_text}
    You are an expert fill in the blanks maker. Given the above text, it is your job to \
    create a quiz of {number} fill in the blank questions for {subject} students in {tone} tone. 
    
    Each question should have 1 or 2 or 3 or 4 blanks give the blanks give randomly blanks for questions 2 or 3 or 4  . Provide only the correct answer for each question.
    
    Here's an example format for one question:
    
    "{'{{"question"}}'}: "The capital of France is _____ and some content _____ and some content?"
    "{'{{"answer"}}'}: "{"ansewer""answer""answer"}" the output should be in json
    
    Please follow this format for each question. and give me in array
    """
    
    TEMPLATE2 = f"""
    You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
    You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
    
    If the quiz is not at par with the cognitive and analytical abilities of the students,\
    update the quiz questions which need to be changed and change the tone to fit the students' abilities perfectly.
    
    Quiz_MCQs:
    {{quiz}}
    
    Check from an expert English Writer of the above quiz:
    """

    

    quiz_generation_prompt = PromptTemplate(
        input_variables=[ "number", "subject", "tone", "response_json"],
        template=TEMPLATE
    )

    quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz")
    
    quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE)
    review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)
    generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=[ "number", "subject", "tone","response_json" ],
                                        output_variables=["quiz", "review"], verbose=True,)
    # Generate the quiz using the chain
    response = generate_evaluate_chain({
        
        "number": number,
        "subject": subject,
        "tone": tone,
        "response_json": json.dumps(RESPONSE_JSON)
    })
    #quiz=response.get("quiz")
# Assume response.get("quiz") is supposed to return a JSON string
    quiz_json = response.get("quiz")
    quiz_data = json.loads(quiz_json)

# Check if quiz_json is None or empty and ensure it is a valid JSON string
    return quiz_data




