# forms.py
from django import forms
from .models import Student,Teacher

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'password', 'roll_number']  # Make sure roll_number is included

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'password', 'subject']  # Make sure roll_number is included