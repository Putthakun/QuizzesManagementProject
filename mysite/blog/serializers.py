from rest_framework import serializers
from rest_framework import viewsets
from django.contrib.auth.hashers import make_password
from .models import *


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['user_type', 'firstname', 'lastname', 'password']
        extra_kwargs = {'password': {'write_only': True}}

#register student
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['user_type', 'firstname', 'lastname', 'password', 'student_id']
        extra_kwargs = {'password': {'write_only': True}}  # ทำให้รหัสผ่านไม่แสดงใน response

        def validate_student_id(self, value):
            if Student.objects.filter(student_id=value).exists():
                raise serializers.ValidationError("Student ID already exists.")
            return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        student = Student.objects.create(**validated_data)
        return student

#register teacher
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['user_type', 'firstname', 'lastname', 'password', 'teacher_id']
        extra_kwargs = {'password': {'write_only': True}}  # ทำให้รหัสผ่านไม่แสดงใน response

        def validate_teacher_id(self, value):
            if Teacher.objects.filter(teacher_id=value).exists():
                raise serializers.ValidationError("Teacher ID already exists.")
            return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        teacher = Teacher.objects.create(**validated_data)
        return teacher

class SubjectSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField()  # หรือสร้าง serializer สำหรับ Teacher model

    class Meta:
        model = Subject
        fields = [ 'code', 'name', 'teacher']


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['subject_code', 'title', 'description', 'due_date', 'score']

    def validate_score(self, value):
        if value < 0:
            raise serializers.ValidationError("Score must be a non-negative value.")
        return value

    def validate_due_date(self, value):
        # ตรวจสอบว่า due_date ต้องมากกว่าปัจจุบัน
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date must be in the future.")
        return value
