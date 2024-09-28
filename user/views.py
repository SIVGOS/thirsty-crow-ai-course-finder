from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Topic

def logout_view(request):
    if not request.user.is_anonymous:
        logout(request)
    return redirect('/login/')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    elif request.method == 'POST':
        user = authenticate(username=request.POST.get('email'),
                            password=request.POST.get('password'))
        if user is None:
            return render(request, 'signin.html', {'message': 'Invalid email or password'})
        else:
            login(request, user)
            topics = Topic.objects.filter(user=user)
            request.method = 'get'
            if not topics:
                return redirect('/topic/')
            return redirect('/dashboard/')
        

@login_required(login_url='/login/')
def topic_view(request):
    if request.method == 'GET':
        return render(request, 'topic_form.html')
    elif request.method == 'POST':
        topic = Topic.objects.create(
            user=request.user,
            topic=request.POST.get('topic'),
            experience_level=request.POST.get('experience_level'),
            dedication=request.POST.get('dedication')
        )
        print('Topic created')
        return HttpResponse('Topic created')

@login_required(login_url='/login/') 
def password_reset(request):
    if request.method == 'GET':
        return render(request, )
