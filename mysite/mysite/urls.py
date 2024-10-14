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
#from blog.views import *
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.hello, name='hello_page'),
    path("register/", views.register, name="register"),
    path("person/", views.person_list.as_view(), name="person_list"),
    path("student/", views.student_list.as_view(), name="student_list"),
    path("teacher/", views.teacher_list.as_view(), name="teacher_list"),
    path("home/", views.home, name=""),

]
