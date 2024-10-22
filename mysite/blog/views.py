from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login
from django.contrib import messages
#form.py
from .forms import StudentForm, TeacherForm
#model.py
from .models import *

import hashlib


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

#Hash password 
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# register
def register(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')  # Get the user type from the form
        if user_type == 'student':
            form = StudentForm(request.POST)
            if form.is_valid():
                student = form.save(commit=False)  
                student.password = hash_password(form.cleaned_data['password'])  # เข้ารหัสรหัสผ่าน
                student.save()  # Save the student data
                return redirect('login')  # Redirect to the login page
        elif user_type == 'teacher':
            form = TeacherForm(request.POST)
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
                    return redirect('home_page')
                else:
                    error_message = "Invalid student ID or password."
            except Student.DoesNotExist:
                error_message = "Student not found."

        elif user_type == 'teacher':
            teacher_id = request.POST.get('teacher_id')
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
                    return redirect('home_page')
                else:
                    error_message = "Invalid teacher ID or password."
            except Teacher.DoesNotExist:
                error_message = "teacher not found."

        return render(request, 'blog/login_page.html', {'error_message': error_message})

    return render(request, 'blog/login_page.html')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()