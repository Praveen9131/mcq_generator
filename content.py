import os
import json
from flask import Flask, request, jsonify
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
KEY = os.getenv("OPENAI_API_KEY")
def generate_content(topic, no_words):
    llm = ChatOpenAI(openai_api_key=KEY, model_name="gpt-4", temperature=1.0)
    
    predefined_text = f"Based on the fundamentals of {topic}, create a content that encompasses the core concepts and challenges students' understanding."
    
    TEMPLATE = f"""
    Text: {predefined_text}
    You are an expert content generator. Given the above text, your task is to create content about {topic} with {no_words} words.
    Ensure that the content covers the core concepts and engages the readers effectively.
    """

    quiz_generation_prompt = PromptTemplate(
        input_variables=["topic", "no_words"],
        template=TEMPLATE
    )

    quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="content")
    
    quiz_evaluation_prompt = PromptTemplate(input_variables=["topic", "no_words"], template=TEMPLATE)
    review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)
    
    generate_evaluate_chain = SequentialChain(
        chains=[quiz_chain, review_chain],
        input_variables=["topic", "no_words"],
        output_variables=["content", "review"],
        verbose=True
    )

    response = generate_evaluate_chain({
        "topic": topic,
        "no_words": no_words
    })

    print("Response:", response)  # Add this print statement

    
    content_json = response.get("content")
    if content_json:
        
        content_without_newlines = content_json.replace("\n", "")
        return content_without_newlines
    else:
        return None

    


    #return content_json



@app.route('/generate', methods=['GET',"POST"])
def generate():
    topic = request.args.get('topic')
    no_words = request.args.get('no_words')
    if topic and no_words:
        content = generate_content(topic, no_words)
        if content:
            return jsonify({"content": content})
        else:
            return jsonify({"error": "Content could not be generated"}), 500
    else:
        return jsonify({"error": "Topic and number of words are required"}), 400

if __name__ == '__main__':
    app.run(debug=True,port=5001)
