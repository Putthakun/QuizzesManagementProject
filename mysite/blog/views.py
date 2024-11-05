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
import logging
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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            # คืนค่า ID ของ exam ที่ถูกสร้าง
            return Response({"id": serializer.data['id']}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
    

    
class QuestionCreateView(generics.CreateAPIView):
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)  # รับข้อมูลคำถามหลายข้อ
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ExamQuestionsView(APIView):
    def get(self, request, exam_id):
        try:
            # ตรวจสอบว่า Exam มีอยู่จริงหรือไม่
            exam = Exam.objects.get(id=exam_id)
        except Exam.DoesNotExist:
            return Response({"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)

        # ดึง Questions ทั้งหมดที่เชื่อมกับ Exam ที่ระบุ
        questions = Question.objects.filter(exam=exam).order_by('order')
        serializer = QuestionSerializer(questions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UpdateQuestionsView(APIView):
    def put(self, request):
        data = request.data
        questions_data = data.get('questions', [])

        for question_data in questions_data:
            question_id = question_data.get('id')
            try:
                question = Question.objects.get(id=question_id)
                serializer = QuestionSerializer(question, data=question_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Question.DoesNotExist:
                return Response({"error": f"Question with id {question_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Questions updated successfully."}, status=status.HTTP_200_OK)
    
@api_view(['PUT', 'PATCH'])
def update_questions(request):
    quiz_data = request.data
    logging.info(f"Received data: {quiz_data}")  # เพิ่ม log สำหรับตรวจสอบข้อมูลที่ได้รับ

    for question_data in quiz_data:
        question_id = question_data.get('exam_id')
        logging.info(f"Processing question ID: {question_id}")  # log question ID
        try:
            question = Question.objects.get(id=question_id)
            question_serializer = QuestionUpdateSerializer(question, data=question_data, partial=True)
            if question_serializer.is_valid():
                question_serializer.save()
            else:
                logging.error(f"Question serializer errors: {question_serializer.errors}")  # log ข้อผิดพลาด
                return Response(question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            for choice_data in question_data.get('choices', []):
                choice_id = choice_data.get('id')
                if choice_id:
                    try:
                        choice = Choice.objects.get(id=choice_id, question=question)
                        choice_serializer = ChoiceSerializer(choice, data=choice_data, partial=True)
                        if choice_serializer.is_valid():
                            choice_serializer.save()
                        else:
                            logging.error(f"Choice serializer errors: {choice_serializer.errors}")  # log ข้อผิดพลาด
                            return Response(choice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    except Choice.DoesNotExist:
                        return Response({'error': 'Choice not found'}, status=status.HTTP_404_NOT_FOUND)

        except Question.DoesNotExist:
            return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'message': 'Questions and choices updated successfully'}, status=status.HTTP_200_OK)

