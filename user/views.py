from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserSubject

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
            request.method = 'get'
            if not UserSubject.objects.filter(user=user).exists():
                print('###########')
                return redirect('/subject/')
            return redirect('/dashboard/')

@login_required(login_url='/login/') 
def password_reset(request):
    if request.method == 'GET':
        return HttpResponse('In progress')
