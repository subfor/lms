from django.shortcuts import render
from django.http import HttpResponse
from academy.models import Student, Lecturer, Group


def get_index(request):
    return render(request, 'academy/start.html')


def get_students(request):
    students = Student.objects.all().order_by('student')
    return render(request, 'academy/students.html', {'students': students})


def get_lecturers(request):
    lecturers = Lecturer.objects.all().order_by('teacher_id')
    return render(request, 'academy/lecturers.html', {'lecturers': lecturers})


def get_groups(request):
    groups = Group.objects.all().order_by('group')
    return render(request, 'academy/groups.html', {'groups': groups})
