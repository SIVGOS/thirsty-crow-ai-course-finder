from django.shortcuts import render, redirect, HttpResponse
from .helpers import get_sub_topics
from django.urls import reverse
from .forms import SubjectForm
from user.models import UserSubject, UserTopic
from .models import Subject, Topic
from constants import GET, POST
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/') 
def create_subject(request):
    if request.method == POST:
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject_name = form.cleaned_data['subject_name']
            experience_code = form.cleaned_data['experience_code']
            dedication_code = form.cleaned_data['dedication_code']

            subject, created = Subject.objects.get_or_create(
                subject_name=subject_name,
                experience_code=experience_code,
                dedication_code=dedication_code
            )
            user_subject = UserSubject.objects.create(
                user=request.user,
                subject=subject
            )

            topics = Topic.objects.filter(subject=subject)
            if not topics:
                print('Generating topics...')
                topics = get_sub_topics(subject)
            request.method = GET
            return render('topics.html', {'topics': topics})
    else:
        form = SubjectForm()
    
    return render(request, 'create_subject.html', {'form': form})
