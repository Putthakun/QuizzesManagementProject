# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.models import *


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user_type','name', 'password','student_id']  # Make sure roll_number is included

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['user_type','teacher_id','name', 'password']  # Make sure roll_number is included


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['code', 'name']