from academy.forms import AddGroupForm, AddLecturerForm, AddStudentForm
from academy.models import Group, Lecturer, Student

from django.shortcuts import render


def get_index(request):
    return render(request, 'academy/start.html')


def get_students(request):
    students = Student.objects.all().order_by('-student')
    return render(request, 'academy/students.html', {'students': students})


def get_lecturers(request):
    lecturers = Lecturer.objects.all().order_by('-teacher_id')
    return render(request, 'academy/lecturers.html', {'lecturers': lecturers})


def get_groups(request):
    groups = Group.objects.all().order_by('-group')
    return render(request, 'academy/groups.html', {'groups': groups})


def add_student(request):
    student = None
    message = ""
    if request.method == 'POST':
        add_student_form = AddStudentForm(data=request.POST)
        if add_student_form.is_valid():
            student = add_student_form.save()
            message = f"Student {student.first_name} {student.last_name} successfully added to LMS"
    context = {
        'student': student,
        'add_student_form': AddStudentForm(),
        'message': message
    }

    return render(request, 'academy/add_student.html', context)


def add_lecturer(request):
    lecturer = None
    message = ""
    if request.method == 'POST':
        add_lecturer_form = AddLecturerForm(data=request.POST)
        if add_lecturer_form.is_valid():
            lecturer = add_lecturer_form.save()
            message = f"Lecturer {lecturer.first_name} {lecturer.last_name} successfully added to LMS"
    context = {
        'lecturer': lecturer,
        'add_lecturer_form': AddStudentForm(),
        'message': message
    }

    return render(request, 'academy/add_lecturer.html', context)


def add_group(request):
    group = None
    message = ""
    if request.method == 'POST':
        add_group_form = AddGroupForm(data=request.POST)
        if add_group_form.is_valid():
            group = add_group_form.save()
            message = f"Group {group.group_name} successfully added to LMS"

    context = {
        'group': group,
        'add_group_form': AddGroupForm(),
        'message': message
    }

    return render(request, 'academy/add_group.html', context)
