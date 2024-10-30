import os

GET='GET'
POST='POST'
DELETE='DELETE'
GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')
GEMINI_DEFAULT_MODEL_NAME='gemini-1.5-flash'
GEMINI_MODEL_NAME=os.getenv('GEMINI_MODEL_NAME', GEMINI_DEFAULT_MODEL_NAME)
YOUTUBE_API_KEY=os.getenv('YOUTUBE_API_KEY')
YOUTUBE_API_SERVICE_NAME='youtube'
YOUTUBE_API_VERSION='v3'
YOUTUBE_URL_FORMAT='https://www.youtube.com/watch?v={video_id}'

if not GEMINI_API_KEY:
    raise Exception('GEMINI_API_KEY must be present in enviroment')

if not YOUTUBE_API_KEY:
    raise Exception('YOUTUBE_API_KEY must be present in enviroment')

LOGIN_MSG = {
    '0': 'Logged out successfully',
    '1': 'Password changed. Please log in with your new password'
}

LOADER_SETTINGS = {
    '0': {
        'message': 'Finding topics. Please wait.',
        'callback_url': '/topic/track/?tracking_id={tracking_id}',
        'success_url': '/topic/?subject_id={obj_id}'
    }
}

class ProcessingStatus:
    PROCESSED = 'PROCESSED'
    PROCESSING = 'PROCESSING'

class CourseFindStatus:
    PENDING = 'PENDING'
    FOUND = 'FOUND'
    SELECTED = 'SELECTED'

