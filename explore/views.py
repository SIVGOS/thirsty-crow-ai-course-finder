from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError
from user.models import UserSubject, UserTopic
from .models import Subject, Topic
from .tasks import populate_topics, populate_videos
from .utils import clean_subject_data
from config import GET, POST, LOADER_SETTINGS, CourseFindStatus
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/') 
def create_subject(request):
    if request.method == GET:
        return render(request, 'create_subject.html')
    
    subject_name, experience_code, dedication_code = clean_subject_data(request.POST)

    subject, created = Subject.objects.get_or_create(
            subject_name=subject_name,
            experience_code=experience_code,
            dedication_code=dedication_code
        )

    try:
        user_subject = UserSubject.objects.get_or_create(
            user=request.user,
            subject=subject
        )
    except IntegrityError:
        pass

    request.method = GET

    if subject.topics_created:
        return redirect(f'/topics?subject_id={subject.id}')
    populate_topics.delay(subject.id)
    return redirect(f'/loader/?tracking_id={subject.tracking_id}')

@api_view(http_method_names=[GET])
def track_topic_creation(request):
    tracking_id = request.GET.get('tracking_id')
    if not tracking_id:
        return Response({'message': 'No subject id provided'}, status=status.HTTP_400_BAD_REQUEST)
    subject = Subject.objects.filter(tracking_id=tracking_id).first()
    if not subject:
        return Response({'message': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)
    if subject.topics_created is True:
        return Response({'message': 'Topics created', 'subject_id': subject.id}, status=status.HTTP_200_OK)
    return Response({'message': 'Topic not created'}, status=status.HTTP_204_NO_CONTENT)

@login_required(login_url='/login/') 
def loader_view(request):
    tracking_id = request.GET.get('tracking_id')
    return render(request, 'loader.html', {'tracking_id': tracking_id})

@login_required(login_url='/login/') 
def topic_confidence_view(request):
    if request.method == GET:
        subject_id = request.GET.get('subject_id')
        topics = Topic.objects.filter(subject_id=subject_id)
        return render(request, 'topics.html', {'subject_id': subject_id, 'topics': topics})
    
    subject_id = int(request.POST.get('subject_id'))
    for key, value in request.POST.items():
        if key.startswith('score_'):
            topic_id = int(key.split('_')[1])
            UserTopic.objects.create(
                user=request.user,
                topic_id=topic_id,
                confidence_level=int(value),
                course_find_status=CourseFindStatus.PENDING)
    
    user_subject = UserSubject.objects.filter(
            user=request.user,
            subject_id=subject_id
            ).first()
    populate_videos.delay(user_subject.id)
    
    request.method = GET
    return redirect('/dashboard/')

