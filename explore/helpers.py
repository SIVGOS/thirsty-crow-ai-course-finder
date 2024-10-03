import os, json
from dotenv import load_dotenv
import datetime as dt
import google.generativeai as genai
from googleapiclient.discovery import build
from .models import Subject, Topic, YoutubeVideo
from user.models import UserTopic
from .template_utils import GET_SUB_TOPICS, VIDEO_SEARCH_TEMPLATE, get_confidence_keyword
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

def get_video_for_topic(topic: UserTopic):
    keyword = VIDEO_SEARCH_TEMPLATE.format(
        topic_name=topic.topic.topic_name,
        subject_name=topic.topic.subject.subject_name,
        experience=get_confidence_keyword(topic.confidence_level)
    )
    videos = search_youtube_videos(keyword)
    video_ids = []
    for video in videos:
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



        