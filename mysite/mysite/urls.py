"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
#from blog.views import *
from blog import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("home/", views.home, name="home"),
    path("subject/", views.subject, name=""),
    path("home_page/", views.home_page, name="home_page"),
    path("subject_page/", views.subject_page, name="subject_page"),
    path("take_test_page/", views.take_test_page, name="take_test_page"),
    path("multi_page/", views.multi_page, name="multi_page"),
    path("home_page_teacher/", views.home_page_teacher, name="home_page_teacher"),

]
