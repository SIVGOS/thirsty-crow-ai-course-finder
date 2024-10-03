"""
URL configuration for course_master project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import user.views as user_views
import explore.views as exp_views


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('login/', user_views.login_view, name='login'),
    path('dashboard/', user_views.dashboard, name='dashboard'),
    path('logout/', user_views.logout_view, name='logout'),
    path('password/reset/', user_views.password_reset, name='reset_password'),
    path('subject/', exp_views.create_subject, name='subject'),
    path('topic/', exp_views.get_sub_topics),
    path('subject/track/', user_views.get_status)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

