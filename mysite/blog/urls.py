from django.urls import path
from .views import *

urlpatterns = [
    path('register/students/', StudentRegisterView.as_view(), name='register'),
    path('register/teacher/', TeacherRegisterView.as_view(), name='teacher'),
    path('login/', login_view, name='login'),
    path('check_session',check_session, name='check_session'),  
]
