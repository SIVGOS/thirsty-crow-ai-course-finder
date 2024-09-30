import os, json
from dotenv import load_dotenv
import google.generativeai as genai
from .models import Subject, Topic
from .prompt_templates import GET_SUB_TOPICS

gemini_api_key = os.getenv('GEMINI_API_KEY')

if not gemini_api_key:
    raise Exception('GEMINI_API_KEY must be present in enviroment')

genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

def get_sub_topics(subject: Subject):
    prompt = GET_SUB_TOPICS.format(
        subject_name = subject.subject_name,
        experience = subject.get_experience_display(),
        dedication = subject.get_dedication_display()
    )
    response = model.generate_content(prompt)
    topics = json.loads(response.text)
    topic_objects = []
    for topic in topics:
        topic = Topic.objects.create(
                            subject=subject,
                            topic_name=topic['topic_name'],
                            description=topic['description']
                        )
        topic_objects.append(topic)
    
    return topic_objects
