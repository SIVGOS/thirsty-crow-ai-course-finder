import os, json
from dotenv import load_dotenv
import datetime as dt
import google.generativeai as genai
from googleapiclient.discovery import build
import youtube_transcript_api
from .models import Subject, Topic, YoutubeVideo, YoutubeVideoSummary
from user.models import UserTopic, UserSubject
from .template_utils import GET_SUB_TOPICS, VIDEO_SEARCH_TEMPLATE, get_confidence_keyword, VIDEO_SUMMARIZE_PROMPT_TEMPLATE
from constants import (GEMINI_API_KEY, GEMINI_MODEL_NAME,
                       YOUTUBE_API_KEY, YOUTUBE_API_SERVICE_NAME,  YOUTUBE_API_VERSION)

genai.configure(api_key=GEMINI_API_KEY)

def get_sub_topics(subject: Subject):
    model = genai.GenerativeModel(GEMINI_MODEL_NAME)
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


def search_youtube_videos(query:str, max_results:int=5, order:str='relevance'):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)

    # Search for videos with sorting by upload date
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_results,
        type='video',  # Only search for videos
        order=order,  # Sort by upload date
        relevanceLanguage='en'
    ).execute()

    videos = []
    for item in search_response.get('items', []):
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        upload_date = item['snippet']['publishedAt']  # Get the upload date
        
        # Get video statistics (views and likes)
        video_stats = youtube.videos().list(
            part='statistics',
            id=video_id
        ).execute()

        stats = video_stats.get('items', [])[0]['statistics']
        view_count = stats.get('viewCount', 'N/A')
        like_count = stats.get('likeCount', 'N/A')

        # Append a dictionary for each video
        videos.append({
            'title': title,
            'video_id': video_id,
            'upload_date': dt.datetime.strptime(upload_date, '%Y-%m-%dT%H:%M:%SZ').date(),
            'views': int(view_count),
            'likes': int(like_count)
        })

    return videos

def check_or_create_video_summary(video_id, video_title):
    if YoutubeVideoSummary.objects.filter(video_id=video_id).exists():
        return True
    try:
        transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = [z.get('text', '') for z in transcript]
        transcript_text = '\n'.join([z.strip() for z in transcript_text if z.strip()])
    except Exception as e:
        print('Failed transcript generation:', str(e))
        return False
    
    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        prompt = VIDEO_SUMMARIZE_PROMPT_TEMPLATE.format(
            video_title=video_title,
            transcript_text=transcript_text
        )
        resp = model.generate_content(prompt)
        video_summary = resp.text
        YoutubeVideoSummary.objects.create(video_id=video_id, summary=video_summary)
        return True
    except Exception as e:
        print('Video transcript exists but LLM agent failed to generate summary')
        print('Exception:', str(e))
        return False
    

def get_videos_for_topic(topic: UserTopic):
    keyword = VIDEO_SEARCH_TEMPLATE.format(
        topic_name=topic.topic.topic_name,
        subject_name=topic.topic.subject.subject_name,
        experience=get_confidence_keyword(topic.confidence_level)
    )
    videos = search_youtube_videos(keyword, max_results=10)
    video_ids = []
    for video in videos:
        video_id = video['video_id']
        video_title = video['title']

        if not check_or_create_video_summary(video_id, video_title):
            print(f'Skipping video "{video_title}" as it does not have a summary')
            continue

        yt_video, created = YoutubeVideo.objects.get_or_create(
            topic=topic.topic,
            video_key=video['video_id'],
            video_title=video['title']
        )

        yt_video.likes_count = video['likes']
        yt_video.views_count = video['views']
        yt_video.uploaded_on = video['upload_date']
        yt_video.save()
        video_ids.append(yt_video.id)
    
    return video_ids

