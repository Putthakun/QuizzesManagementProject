from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password

#model.py
from .models import *

import hashlib

import re


# Create your views here.

def hello(request):
    return render(request, 'blog/hello.html')

def home(request):
    return render(request, 'blog/home.html')

def subject(request):
    return render(request, 'blog/subject.html')

def home_page(request):
        return render(request, 'blog/home_page.html')
 
def subject_page(request):
    return render(request, 'blog/subject_page.html')

def take_test_page(request):
    return render(request, 'blog/take_test_page.html')

def multi_page(request):
    return render(request, 'blog/multi_page.html')

def home_page_teacher(request):
     # ตรวจสอบให้แน่ใจว่าผู้ใช้ได้เข้าสู่ระบบผ่าน session
    user_id = request.session.get('user_id')  # ดึง user_id จาก session
    if user_id:
        try:
            # ดึงข้อมูลอาจารย์ตาม user_id ที่เก็บใน session
            teacher = Teacher.objects.get(id=user_id)
            # ดึงข้อมูลวิชาที่เชื่อมโยงกับอาจารย์
            subjects = teacher.subjects.all()  # ใช้ related_name 'subjects'
            return render(request, 'blog/home_page_teacher.html', {'subjects': subjects})
        except Teacher.DoesNotExist:
            # หากไม่พบอาจารย์ในฐานข้อมูล
            return redirect('login')  # ส่งผู้ใช้ไปยังหน้าเข้าสู่ระบบ
    else:
        # หากยังไม่ได้เข้าสู่ระบบ อาจส่งผู้ใช้ไปยังหน้าเข้าสู่ระบบ
        return redirect('login')  # เปลี่ยนเป็นชื่อ URL ที่ถูกต้อง

def choice_page(request):
    return render(request, 'blog/choice_page.html')


#Register student
class StudentRegisterView(generics.CreateAPIView):
    serializer_class = StudentSerializer

#Register teacher
class TeacherRegisterView(generics.CreateAPIView):
    serializer_class = TeacherSerializer

@api_view(['POST'])
def login_view(request):
    user_type = request.data.get('user_type')  # รับ user_type (student หรือ teacher)
    user_id = request.data.get('id')           # รับ student_id หรือ teacher_id
    password = request.data.get('password')    # รับรหัสผ่าน

    if user_type == 'student':
        try:
            user = Student.objects.get(student_id=user_id)
            if check_password(password, user.password):  # ตรวจสอบรหัสผ่าน
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": {"password": ["Invalid credentials"]}}, status=status.HTTP_401_UNAUTHORIZED)
        except Student.DoesNotExist:
            return Response({"error": {"student_id": ["Student ID not found"]}}, status=status.HTTP_404_NOT_FOUND)
    elif user_type == 'teacher':
        try:
            user = Teacher.objects.get(teacher_id=user_id)
            if check_password(password, user.password):  # ตรวจสอบรหัสผ่าน
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": {"password": ["Invalid credentials"]}}, status=status.HTTP_401_UNAUTHORIZED)
        except Teacher.DoesNotExist:
            return Response({"error": {"teacher_id": ["Teacher ID not found"]}}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": {"user_type": ["Invalid user type"]}}, status=status.HTTP_400_BAD_REQUEST)
