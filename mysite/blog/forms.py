# forms.py
from django import forms
from .models import Student,Teacher

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user_type','name', 'password','student_id']  # Make sure roll_number is included

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['user_type','teacher_id','name', 'password', 'subject_id']  # Make sure roll_number is included