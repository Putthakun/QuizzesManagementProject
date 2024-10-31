from django.db import models

# Create your models here.
# models.py
from django.db import models
from django.contrib.auth.models import User

from django.core.validators import RegexValidator

# Create your models here.
class Person(models.Model):
    user_type = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.user_type} - {self.name}"

class Student(Person):
    student_id_validator = RegexValidator(
        regex=r'^\d+$',
        message="Student ID must be numeric."
    )
    student_id = models.CharField( max_length=16,
                                      validators=[student_id_validator],
                                      unique=True)
    

    def __str__(self):
        return f"{self.name} - {self.student_id}"  # คืนค่าเป็น string

class Teacher(Person):
    teacher_id_validator = RegexValidator(
        regex=r'^\d+$',
        message="teacher ID must be numeric."
    )
    teacher_id = models.CharField(max_length=16,
                                      validators=[teacher_id_validator],
                                      unique=True)

    def __str__(self):
        return f"{self.name} - {self.teacher_id}"  # คืนค่าเป็น string


class Subject(models.Model):
    code = models.CharField(max_length=8)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name