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
        fields = ['id', 'subject_code', 'title', 'description', 'due_date', 'score',]

    def validate_score(self, value):
        if value < 0:
            raise serializers.ValidationError("Score must be a non-negative value.")
        return value

    def validate_due_date(self, value):
        # ตรวจสอบว่า due_date ต้องมากกว่าปัจจุบัน
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date must be in the future.")
        return value


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)  # ใช้ Choice serializer แบบซ้อน
    exam_id = serializers.IntegerField(write_only=True)  # ใช้ exam_id เพื่อเชื่อมกับข้อสอบที่มีอยู่แล้ว

    class Meta:
        model = Question
        fields = ['id', 'exam_id', 'question_text', 'points', 'order', 'choices']

    def create(self, validated_data):
        choices = ChoiceSerializer(many=True)
        choices_data = validated_data.pop('choices')
        exam_id = validated_data.pop('exam_id')  # ดึง exam_id ที่ส่งมาเพื่อสร้างการเชื่อมโยงกับข้อสอบ
        
        # ตรวจสอบว่า exam_id มีอยู่ในฐานข้อมูลหรือไม่
        try:
            exam = Exam.objects.get(id=exam_id)
        except Exam.DoesNotExist:
            raise serializers.ValidationError({"exam_id": "Exam with this ID does not exist."})
        
        # สร้างคำถามที่เชื่อมโยงกับ Exam
        question = Question.objects.create(exam=exam, **validated_data)
        
        # สร้างตัวเลือกที่เชื่อมโยงกับ Question ที่สร้างขึ้นใหม่
        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)
        return question
    
    def update(self, instance, validated_data):
        choices_data = validated_data.pop('choices', [])
        instance.question_text = validated_data.get('question_text', instance.question_text)
        instance.points = validated_data.get('points', instance.points)
        instance.order = validated_data.get('order', instance.order)
        instance.save()

        # ลบ choices ที่มีอยู่ทั้งหมด
        instance.choices.all().delete()

        # สร้าง choices ใหม่
        for choice_data in choices_data:
            Choice.objects.create(question=instance, **choice_data)

        return instance
    
class QuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'  # หรือระบุฟิลด์ที่ต้องการ
    