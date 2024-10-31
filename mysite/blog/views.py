from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login
from django.contrib import messages
#form.py
from .forms import *
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

#Hash password 
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# register
def register(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')  # Get the user type from the form
        if user_type == 'student':
            form = StudentForm(request.POST)

            student_id = request.POST.get('student_id')
            if not re.match(r'^\d+$', student_id):                                 # regular expression
                 messages.error(request, "Student ID must be numeric.")
                 return render(request, 'blog/register.html', {'form': form})
            
            name = request.POST.get('name')
            if not re.match(r'^[A-Za-z\s]+$', name):                                 # regular expression
                 messages.error(request, "Name must be English only.")
                 return render(request, 'blog/register.html', {'form': form})
            
            if form.is_valid():
                student = form.save(commit=False)  
                student.password = hash_password(form.cleaned_data['password'])  # เข้ารหัสรหัสผ่าน
                student.save()  # Save the student data
                return redirect('login')  # Redirect to the login page
        elif user_type == 'teacher':
            form = TeacherForm(request.POST)
            teacher_id = request.POST.get('teacher_id')

            if not re.match(r'^\d+$', teacher_id):                              # regular expression
                 messages.error(request, "teacher ID must be numeric.")
                 return render(request, 'blog/register.html', {'form': form})
            
            name = request.POST.get('name')
            if not re.match(r'^[A-Za-z\s]+$', name):                                 # regular expression
                 messages.error(request, "Name must be English only.")
                 return render(request, 'blog/register.html', {'form': form})
            
            if form.is_valid():
                teacher = form.save(commit=False) 
                teacher.password = hash_password(form.cleaned_data['password'])  # เข้ารหัสรหัสผ่าน
                teacher.save()  # Save the teacher data
                return redirect('login')  # Redirect to the login page
    else:
        form = StudentForm()  # Default to StudentForm

    return render(request, 'blog/register.html', {'form': form})

#login
from .models import Student
def login(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')

        if user_type == 'student':
            student_id = request.POST.get('student_id')
            if not re.match(r'^\d+$', student_id):                          # regular expression
                 messages.error(request, "Student ID must be numeric.")
                 return render(request, 'blog/login_page.html')
            
            raw_password = request.POST.get('password')
            try:
                # fide stdent_id
                student = Student.objects.get(student_id=student_id)
                
                # Hash password
                hashed_password = hash_password(raw_password)
                
                # Check password
                if student.password == hashed_password:
                    # Session
                    request.session['user_id'] = student.id
                    request.session['username'] = student.name
                    return redirect('home_page')
                else:
                    error_message = "Invalid student ID or password."
            except Student.DoesNotExist:
                error_message = "Student not found."

        elif user_type == 'teacher':
            teacher_id = request.POST.get('teacher_id')
            if not re.match(r'^\d+$', teacher_id):                         # regular expression
                 messages.error(request, "teacher ID must be numeric.")
                 return render(request, 'blog/login_page.html')
            raw_password = request.POST.get('password')
            try:
                # fide teacher_id
                teacher = Teacher.objects.get(teacher_id=teacher_id)
                
                # Hash password
                hashed_password = hash_password(raw_password)
                
                # Check password
                if teacher.password == hashed_password:
                    # Session
                    request.session['user_id'] = teacher.id
                    request.session['username'] = teacher.name
                    return redirect('home_page_teacher')
                else:
                    error_message = "Invalid teacher ID or password."
            except Teacher.DoesNotExist:
                error_message = "teacher not found."

        return render(request, 'blog/login_page.html', {'error_message': error_message})

    return render(request, 'blog/login_page.html')

#hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#create subject
def create_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)  # สร้าง Subject แต่ยังไม่บันทึกลงฐานข้อมูล
             # ดึงข้อมูลอาจารย์ที่เกี่ยวข้องกับผู้ใช้ที่ล็อกอินอยู่
            teacher = Teacher.objects.get(id=request.user.id)
      
            # กำหนดค่า teacher ให้กับวิชาที่สร้าง
            subject.teacher = teacher
            subject.save()  # บันทึก Subject ลงฐานข้อมูล

            messages.success(request, "Subject created successfully")
            return redirect('home_page')  # เปลี่ยนไปยังหน้าที่ต้องการ
        else:
            messages.error(request, "Could not create subject. Please check the form.")
    else:
        form = SubjectForm()
    return render(request, 'blog/home_page_teacher.html', {'form': form})