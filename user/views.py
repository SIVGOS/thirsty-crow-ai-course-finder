from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import F
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UserSubject, UserTopic
from explore.models import YoutubeVideo, YoutubeVideoSummary
from config import GET, POST, DELETE, LOGIN_MSG, YOUTUBE_URL_FORMAT, ProcessingStatus

def logout_view(request):
    if not request.user.is_anonymous:
        logout(request)
    return redirect('/login/?ref=0')

def login_view(request):
    if request.method == GET:
        message = LOGIN_MSG.get(request.GET.get('ref', ''), None)
        return render(request, 'signin.html', {'message': message})

    elif request.method == POST:
        user = authenticate(username=request.POST.get('email'),
                            password=request.POST.get('password'))
        if user is None:
            return render(request, 'signin.html', {'message': 'Invalid email or password'})
        
        login(request, user)
        request.method = GET
        return redirect('/dashboard/')

@login_required(login_url='/login/') 
def password_reset(request):
    if request.method == GET:
        return render(request, 'reset_password.html')
    
    org_password = request.POST.get('org_password')
    new_password1 = request.POST.get('new_password1')
    new_password2 = request.POST.get('new_password2')
    
    if new_password1 != new_password2:
        return render(request, 'reset_password.html', {'message': 'The two passwords must be the same'})
    
    if not request.user.check_password(org_password):
        return render(request, 'reset_password.html', {'message': 'Current password not correct'})
    
    request.user.set_password(new_password1)
    request.user.save()
    logout(request)
    request.method = GET
    return redirect('/login/?ref=1')


def home(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return redirect('/login/')


@login_required(login_url='/login/')
def dashboard(request):
    user_subjects = (
        UserSubject.objects.filter(user=request.user)
        .order_by('-created_on')
        .annotate(subject_name=F('subject__subject_name'))
        .values('id', 'subject_name', 'status', 'tracking_id')
    )

    if not user_subjects:
        return redirect('/subject/')
    
    tracking_ids = '|'.join([str(z['tracking_id']) for z in user_subjects if z['status'] == ProcessingStatus.PROCESSING])
    return render(request, 'dashboard.html', {'subjects': user_subjects, 'tracking_ids': tracking_ids})

@api_view(http_method_names=[GET])
def get_status(request):
    tracking_ids = request.query_params.get('tracking_ids').split('|')
    tracking_statuses = UserSubject.objects.filter(tracking_id__in=tracking_ids).values_list('status', flat=True)
    processing_status = ProcessingStatus.PROCESSING
    if any(z==ProcessingStatus.PROCESSED for z in tracking_statuses):
        processing_status = ProcessingStatus.PROCESSED
    return Response({'status': processing_status}, status=status.HTTP_200_OK)
        

@login_required(login_url='/login/')
def vew_videos(request):
    user_subject = UserSubject.objects.get(id=request.GET.get('id'))
    user_topics = UserTopic.objects.filter(user=request.user, topic__subject=user_subject.subject)
    contexts = {
        'subject': user_subject.subject.subject_name,
        'tracking_key': user_subject.tracking_id,
        'topics': []
        }
    for user_topic in user_topics:
        data = {
            'topic_name': user_topic.topic.topic_name,
            'videos': []
        }
        for video in YoutubeVideo.objects.filter(topic=user_topic.topic):
            video_summary = YoutubeVideoSummary.objects.get(video_id=video.video_key)
            data['videos'].append({
                'id': video.id,
                'title': video.video_title,
                'url': YOUTUBE_URL_FORMAT.format(video_id=video.video_key),
                'uploaded_on': video.uploaded_on,
                'likes': video.likes_count,
                'views': video.views_count,
                'video_summary': video_summary
            })
            contexts['topics'].append(data)
    
    print(contexts)
    return render(request, 'view_subject.html', contexts)

@api_view(http_method_names=[DELETE])
def delete_usersubject(request):
    try:
        tracking_id = request.query_params.get('tracking_id')
        UserSubject.objects.filter(user=request.user, tracking_id=tracking_id).delete()
        return Response({'message': 'deleted'}, status=status.HTTP_200_OK)
    except Exception as ex:
        print(ex)
        return Response({'error': f'{ex}'}, status=status.HTTP_400_BAD_REQUEST)
