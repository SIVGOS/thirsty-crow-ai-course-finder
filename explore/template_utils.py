GET_SUB_TOPICS = """I am learning {subject_name}. {experience}. {dedication}.
Provide the list of top skills that I must learn in a JSON Array format. Each element of the JSON object should be of the following format:
{{
    "topic_name": str,
    "description": str
}}
Don't make any markdown."""


VIDEO_SEARCH_TEMPLATE = "{topic_name} in {subject_name} for {experience} level"


def get_confidence_keyword(confidence_level:int):
    if confidence_level > 3 and confidence_level < 6:
        return 'intermediate'
    if confidence_level > 5:
        return 'advanced'
    return 'beginer'

VIDEO_SUMMARIZE_PROMPT_TEMPLATE = """Generate a brief summary of the youtube video titled "{video_title}" from tha transcript provided below.
Please summarize it in bullet points so that I can quickly skim through the key topics covered in the video.
Video Transcript:
{transcript_text}
"""