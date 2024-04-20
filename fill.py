import os
import json
from flask import Flask, request, jsonify
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
from langchain.chains import SequentialChain
from dotenv import load_dotenv
app=Flask(__name__)
load_dotenv()
KEY = os.getenv("OPENAI_API_KEY")
def generate_quiz1(number, subject, tone):
    llm = ChatOpenAI(openai_api_key=KEY, model_name="gpt-4", temperature=0.5)
    
    # Construct the predefined text for the quiz
    predefined_text = f"Based on the fundamentals of {subject}, create a quiz that encompasses the core concepts and challenges students' understanding."
    RESPONSE_JSON = {
    "": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "": { 
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
}
    


   # Construct the template without using RESPONSE_JSON directly unless it's a variable you pass to LLMChain
    TEMPLATE = f"""
    Text: {predefined_text}
    You are an expert fill in the blanks maker. Given the above text, it is your job to \
    create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
    Make sure the questions are not repeated and check all the questions to be conforming the text as well.
    Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
    Ensure to make {number} MCQs in th forrmate of above variable 
      ,please give me in this format  format of array and generate only fill in the blank question and show only correct answer ,dont show options,you are good at making fill in the blanks questions
      dont generate question numbers , the output should be in array and per question only one blank should be there and dont show and question numbers and text for serial wise
      to esure that show answer for every question ,dont show new line symbols
        "
       ""{"question"}: "The capital of France is _____?",
          {"answer"} follow only this format
       "
    use only this format dont use any other format, the output should be in array and reprsent every element as array object question is one object and answer is one object
       
           
         follow only this format
            // More questions as needed...
      
    """
    TEMPLATE2="""
    You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
    You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
    if the quiz is not at per with the cognitive and analytical abilities of the students,\
    update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
    Quiz_MCQs:
    {quiz}
    
    Check from an expert English Writer of the above quiz:
    """

    quiz_generation_prompt = PromptTemplate(
        input_variables=[ "number", "subject", "tone","response_json"],
        template=TEMPLATE
    )

    quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz")
    
    quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE)
    review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)
    generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=[ "number", "subject", "tone","response_json"],
                                        output_variables=["quiz", "review"], verbose=True,)
    # Generate the quiz using the chain
    response = generate_evaluate_chain({
        
        "number": number,
        "subject": subject,
        "tone": tone,
       "response_json": json.dumps(RESPONSE_JSON)

        
    })
    a=response.get("quiz")
    quiz_data = json.loads(a)
    
 
    
    #quiz=response.get("quiz")


# Check if quiz_json is None or empty and ensure it is a valid JSON string
    return quiz_data



