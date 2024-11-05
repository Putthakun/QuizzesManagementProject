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
from django.urls import path, include
from django.contrib.auth import views as auth_views
#from blog.views import *
from blog import views
from rest_framework.routers import DefaultRouter
from blog.views import SubjectViewSet, StudentRegisterView, TeacherRegisterView, login_view, student_detail, teacher_detail


from blog.views import *
from django.urls import re_path


router = DefaultRouter()
router.register(r'subjects', SubjectViewSet, basename='subject')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # เพิ่มเส้นทาง API สำหรับ SubjectViewSet
    path('login/', login_view, name='login'),
    path('register/students/', StudentRegisterView.as_view(), name='register'),
    path('register/teacher/', TeacherRegisterView.as_view(), name='register_teacher'),
    path('login/', login_view, name='login'),
    path('edit-username/<str:student_id>/', student_detail, name='edit_username'),
    path('edit-username/teacher/<str:teacher_id>/', teacher_detail, name='edit_username_teacher'),


    path('api/teachers/<str:teacher_id>/subjects/', TeacherSubjectsView.as_view(), name='teacher-subjects'),
    path('api/student/<str:student_id>/subjects/', StudentSubjectsView.as_view(), name='student-subjects'),
    path('api/subjects/code/<str:code>/', SubjectDetailByCodeView.as_view(), name='subject_detail_by_code'),
    path('api/exams/', ExamCreateView.as_view(), name='create_exam'),
    path('api/listexams/<str:subject_code>/', ExamListView.as_view(), name='exam-list'),
    path('api/questionCreateView/', QuestionCreateView.as_view(), name='question-create'),
]