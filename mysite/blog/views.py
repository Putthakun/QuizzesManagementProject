from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.generic import ListView
from django.views.generic import TemplateView
from .models import Person, Student, Teacher

# Create your views here.

def hello(request):
    return render(request, 'blog/hello.html')

def register(request):
    return render(request, 'blog/register.html')

def home(request):
    return render(request, 'blog/home.html')

def subject(request):
    return render(request, 'blog/subject.html')

def subject(request):
    return render(request, 'blog/home_page.html')

class person_list(ListView):
    model = Person
    template_name = "person_list.html"  # Specify your template
class student_list(ListView):
    model = Student
    template_name = "student_list.html"  # Specify your template
class teacher_list(ListView):
    model = Teacher
    template_name = "teacher_list.html"  # Specify your template

class person_list_context(TemplateView):
    model = Person
    template_name = "person_list.html"  
    extra_context={'object_list': Person.objects.all()}
class person_student(person_list_context):
    model = Student
    template_name = "student_list.html" 
    extra_context={'object_list': Student.objects.all()}
class person_teacher(person_list_context):
    model = Teacher
    template_name = "teacher_list.html"  
    extra_context={'object_list': Teacher.objects.all()}


from .forms import StudentForm

# views.py
from django.shortcuts import render, redirect
from .forms import StudentForm, TeacherForm

def register(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')  # Get the user type from the form
        if user_type == 'student':
            form = StudentForm(request.POST)
            if form.is_valid():
                form.save()  # Save the student data
                return redirect('student_list')  # Redirect to the student list page
        elif user_type == 'teacher':
            form = TeacherForm(request.POST)
            if form.is_valid():
                form.save()  # Save the teacher data
                return redirect('teacher_list')  # Redirect to the teacher list page
    else:
        form = StudentForm()  # Default to StudentForm

    return render(request, 'blog/register.html', {'form': form})
