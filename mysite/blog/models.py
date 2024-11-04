from django.db import models

# Create your models here.
# models.py
from django.db import models
from django.contrib.auth.models import User

from django.core.validators import RegexValidator

# Create your models here.
class Person(models.Model):
    UERR_TYPE_CHOICES = [
        ('student', 'student'),
        ('teacher', 'teacher'),
    ]
    user_type = models.CharField(max_length=10, choices=UERR_TYPE_CHOICES)
    firstname = models.CharField(max_length=128, default='')
    lastname = models.CharField(max_length=128, default='')
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.user_type} - {self.firstname}"

class Student(Person):
    student_id_validator = RegexValidator(
        regex=r'^\d+$',
        message="Student ID must be numeric."
    )
    student_id = models.CharField(max_length=16,
                                      validators=[student_id_validator],
                                      unique=True)
    

    def __str__(self):
        return f"{self.firstname} - {self.student_id}"  # คืนค่าเป็น string

class Teacher(Person):
    teacher_id_validator = RegexValidator(
        regex=r'^\d+$',
        message="teacher ID must be numeric."
    )
    teacher_id = models.CharField(max_length=16,
                                      validators=[teacher_id_validator],
                                      unique=True)

    def __str__(self):
        return f"{self.firstname} - {self.teacher_id}"  # คืนค่าเป็น string


class Subject(models.Model):
    code = models.CharField(max_length=8)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name
    
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='enrollments')

    class Meta:
        unique_together = ('student', 'subject')  # ไม่ให้นักเรียนลงทะเบียนวิชาเดียวกันซ้ำ

    def __str__(self):
        return f"{self.student} enrolled in {self.subject}"
    

class Exam(models.Model):
    subject_code  = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    title = models.CharField(max_length=255)  # ชื่อข้อสอบ
    description = models.TextField(blank=True)  # รายละเอียดข้อสอบ
    due_date = models.DateField()  # วันครบกำหนดสำหรับข้อสอบ
    score = models.PositiveIntegerField()  # คะแนนสูงสุด

    def __str__(self):
        return f"{self.title} for {self.subject_code.name}"
    
class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')  # เชื่อมกับข้อสอบ
    question_text = models.TextField()  # เนื้อหาของคำถาม
    question_type = models.CharField(max_length=50, choices=[('multiple_choice', 'Multiple Choice'), ('short_answer', 'Short Answer')], default='multiple_choice')  # ประเภทคำถาม
    points = models.PositiveIntegerField(default=1)  # คะแนนของคำถามแต่ละข้อ
    order = models.PositiveIntegerField()  # ลำดับคำถามในข้อสอบ

    def __str__(self):
        return f"Question {self.order} for {self.exam.title}"
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')  # เชื่อมกับคำถาม
    choice_text = models.CharField(max_length=255)  # ตัวเลือกคำตอบ
    is_correct = models.BooleanField(default=False)  # ใช้ระบุว่าตัวเลือกนี้เป็นคำตอบที่ถูกต้องหรือไม่

    def __str__(self):
        return f"Choice for Question {self.question.id}: {self.choice_text}"