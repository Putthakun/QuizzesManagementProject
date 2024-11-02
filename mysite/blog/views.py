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


# Create your views here.
#Register student
class StudentRegisterView(generics.CreateAPIView):
    serializer_class = StudentSerializer

#Register teacher
class TeacherRegisterView(generics.CreateAPIView):
    serializer_class = TeacherSerializer

@api_view(['POST'])
def login_view(request):
    user_type = request.data.get('user_type')  
    user_id = request.data.get('id')           
    password = request.data.get('password')    

    if user_type == 'student':
        try:
            user = Student.objects.get(student_id=user_id)
            if check_password(password, user.password):  # ตรวจสอบรหัสผ่าน
                request.session['user_type'] = 'student'
                request.session['user_id'] = user.student_id
                request.session['firstname'] = user.firstname
                request.session['lastname'] = user.lastname
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": {"password": ["Invalid credentials"]}}, status=status.HTTP_401_UNAUTHORIZED)
        except Student.DoesNotExist:
            return Response({"error": {"student_id": ["Student ID not found"]}}, status=status.HTTP_404_NOT_FOUND)
    elif user_type == 'teacher':
        try:
            user = Teacher.objects.get(teacher_id=user_id)
            if check_password(password, user.password):  # ตรวจสอบรหัสผ่าน
                request.session['user_type'] = 'teacher'
                request.session['user_id'] = user.teacher_id
                request.session['firstname'] = user.firstname
                request.session['lastname'] = user.lastname
                request.session.modified = True  # ทำให้เซสชันถูกบันทึก

                print("Session data before login:")
                print("user_type:", request.session.get('user_type'))
                print("user_id:", request.session.get('user_id'))
                print("firstname:", request.session.get('firstname'))
                print("lastname:", request.session.get('lastname'))

                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": {"password": ["Invalid credentials"]}}, status=status.HTTP_401_UNAUTHORIZED)
        except Teacher.DoesNotExist:
            return Response({"error": {"teacher_id": ["Teacher ID not found"]}}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": {"user_type": ["Invalid user type"]}}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_session(request):
    # ตรวจสอบว่ามีค่าเซสชันหรือไม่
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    firstname = request.session.get('firstname')
    lastname = request.session.get('lastname')
    print("Session data after login:")
    print("user_type:", request.session.get('user_type'))
    print("user_id:", request.session.get('user_id'))
    print("firstname:", request.session.get('firstname'))
    print("lastname:", request.session.get('lastname'))

    if user_type and user_id:  # ตรวจสอบว่ามีข้อมูลเซสชันที่ต้องการ
        return Response({
            "user_type": user_type,
            "user_id": user_id,
            "firstname": firstname,
            "lastname": lastname
        }, status=status.HTTP_200_OK)
    else:
        # หากไม่มีเซสชันให้ส่งข้อความผิดพลาดกลับไป
        return Response({"error": "No active session found"}, status=status.HTTP_401_UNAUTHORIZED)
