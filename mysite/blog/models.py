from django.db import models

# Create your models here.
class Person(models.Model):
    user_type = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    password = models.IntegerField()

    def __str__(self):
        return f"{self.user_type} - {self.name}"

class Student(Person):
    student_id = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.student_id}"  # คืนค่าเป็น string

class Teacher(Person):
    teacher_id = models.IntegerField()
    subject_id = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.teacher_id}"  # คืนค่าเป็น string

    

