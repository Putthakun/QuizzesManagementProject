from django.urls import path
from .views import *

urlpatterns = [
    path('register/students/', StudentRegisterView.as_view(), name='register'),
    path('register/teacher/', TeacherRegisterView.as_view(), name='teacher'),
    path('login/', login_view, name='login'),
    path('set_session/', set_session, name='set_session'),
    path('delete_session/', delete_session, name='delete_session'),
    path('display_session/', get_session, name='display_session'),  # ชื่อที่ใช้ต้องตรงกัน
]
