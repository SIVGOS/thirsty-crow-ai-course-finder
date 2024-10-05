from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import F
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserSubject
from constants import GET, POST, LOGIN_MSG

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
        .values('subject_name', 'status', 'tracking_id')
    )

    if not user_subjects:
        return redirect('/subject/')
    
    tracking_ids = '|'.join([str(z['tracking_id']) for z in user_subjects if z['status'] == 'PROCESSING'])
    return render(request, 'dashboard.html', {'subjects': user_subjects, 'tracking_ids': tracking_ids})

@api_view(http_method_names=[GET])
def get_status(request):
    tracking_id = request.GET.get('tracking_id')
    data = UserSubject.objects.filter(tracking_id=tracking_id).values('status').first()
    return Response(data)
