import os, json
from dotenv import load_dotenv
import google.generativeai as genai
from .prompt_templates import GET_SUB_TOPICS

gemini_api_key = os.getenv('GEMINI_API_KEY')

if not gemini_api_key:
    raise Exception('GEMINI_API_KEY must be present in enviroment')

genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

def get_sub_topics(topic_name, experience, dedication):
    prompt = GET_SUB_TOPICS.format(
        topic_name = topic_name,
        experience = experience,
        dedication = dedication
    )
    
    response = model.generate_content(prompt)
    return json.loads(response.text)
