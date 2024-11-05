from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Person)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Enrollment)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)