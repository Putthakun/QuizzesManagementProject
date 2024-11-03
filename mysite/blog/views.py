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
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from rest_framework import permissions
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
                request.session.modified = True  # ทำให้เซสชันถูกบันทึก
                # ส่งข้อมูลเซสชันกลับไป
                return Response({
                    "message": "Login successful",
                    "user_type": request.session['user_type'],
                    "user_id": request.session['user_id'],
                    "firstname": request.session['firstname'],
                    "lastname": request.session['lastname']
                }, status=status.HTTP_200_OK)
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
                
                # ส่งข้อมูลเซสชันกลับไป
                return Response({
                    "message": "Login successful",
                    "user_type": request.session['user_type'],
                    "user_id": request.session['user_id'],
                    "firstname": request.session['firstname'],
                    "lastname": request.session['lastname']
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": {"password": ["Invalid credentials"]}}, status=status.HTTP_401_UNAUTHORIZED)
        except Teacher.DoesNotExist:
            return Response({"error": {"teacher_id": ["Teacher ID not found"]}}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": {"user_type": ["Invalid user type"]}}, status=status.HTTP_400_BAD_REQUEST)



class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def perform_create(self, serializer):
        teacher_id = self.request.data.get('teacher_id')  # ใช้ teacher_id
        try:
            teacher = Teacher.objects.get(teacher_id=teacher_id)
            serializer.save(teacher=teacher)  
            print("Subject saved successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Teacher.DoesNotExist:
            print("Teacher not found")
            return Response({'error': 'Teacher not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Error saving subject:", e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



