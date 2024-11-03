from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# router = DefaultRouter()
# router.register(r'subjects', SubjectViewSet, basename='subject')

# urlpatterns = [
#     path('register/students/', StudentRegisterView.as_view(), name='register'),
#     path('register/teacher/', TeacherRegisterView.as_view(), name='teacher'),
#     path('login/', login_view, name='login'),
#     path('api/', include(router.urls))
# ]
