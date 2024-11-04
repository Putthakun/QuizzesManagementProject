from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.views import View
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

                teacher_subjects = user.subjects.all()
                subjects_list = [{"code": subject.code, "name": subject.name} for subject in teacher_subjects]
                
                # ส่งข้อมูลเซสชันกลับไป
                return Response({
                    "message": "Login successful",
                    "user_type": request.session['user_type'],
                    "user_id": request.session['user_id'],
                    "firstname": request.session['firstname'],
                    "lastname": request.session['lastname'],
                    "subjects": subjects_list
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
        

class TeacherSubjectsView(generics.ListAPIView):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']  # รับ teacher_id จาก URL
        return Subject.objects.filter(teacher__teacher_id=teacher_id)
    
class StudentSubjectsView(generics.ListAPIView):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        student_id = self.kwargs['student_id']  # รับ student จาก URL
        return Subject.objects.filter(enrollments__student_id=student_id)
    
class SubjectDetailByCodeView(generics.ListAPIView):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        code = self.kwargs['code']  # รับ code จาก URL
        return Subject.objects.filter(code=code)
    

class ExamCreateView(generics.CreateAPIView):
    serializer_class = ExamSerializer

    def create(self, request, *args, **kwargs):
        subject_code = request.data.get('subject_code')  # ดึง subject_code จากข้อมูลที่ส่งมา
        print(f"Received subject_code: {subject_code}")  # ตรวจสอบ subject_code ที่ได้รับ

        # ค้นหา Subject โดยใช้ code
        try:
            subject = Subject.objects.get(code=subject_code)  # ค้นหา Subject ที่มี code ตรงกัน
            print(f"Found subject: {subject}")  # ตรวจสอบว่าพบ Subject หรือไม่
            request.data['subject_code'] = subject.id  # แทนที่ subject_code ด้วย ID ของ Subject
        except Subject.DoesNotExist:
            return Response({"detail": "Subject not found."}, status=status.HTTP_404_NOT_FOUND)

        # เรียกใช้ serializer เพื่อสร้าง Exam
        return super().create(request, *args, **kwargs)


class ExamViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ExamSerializer
    lookup_field = 'subject_code'  # ตั้งค่าให้ใช้ subject_code เป็น lookup field

    def get_queryset(self):
        subject_code = self.kwargs.get('subject_code')  # ดึงค่า subject_code จาก URL
        if subject_code:
            return Exam.objects.filter(subject_code__code=subject_code)  # กรอง Exam ตาม subject_code
        return Exam.objects.all()  # ถ้าไม่มี subject_code ให้คืนค่าทั้งหมด
    

class ExamListView(generics.CreateAPIView):
    def get(self, request, subject_code):
        # Get the Subject instance based on the subject code
        subject = get_object_or_404(Subject, code=subject_code)  # Assume 'code' is the field for subject_code
        # Now use the id of the subject to filter exams
        exams = Exam.objects.filter(subject_code=subject.id).values()
        return JsonResponse(list(exams), safe=False)