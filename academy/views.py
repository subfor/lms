from academy.forms import AddGroupForm, AddLecturerForm, AddStudentForm
from academy.models import Group, Lecturer, Student

from django.shortcuts import get_object_or_404, redirect, render


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
    action_name = "Add student"
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
        'message': message,
        'action_name': action_name
    }

    return render(request, 'academy/add_student.html', context)


def del_student(request, student_id: int):
    student = get_object_or_404(Student, student=student_id)
    student.delete()
    return redirect('students')


def edit_student(request, student_id: int):
    action_name = "Edit student"
    student = get_object_or_404(Student, student=student_id)
    if request.method == 'POST':
        add_student_form = AddStudentForm(request.POST, instance=student)
        if add_student_form.is_valid():
            student = add_student_form.save()
            student.save()
            return redirect('students')
    add_student_form = AddStudentForm(instance=student)
    return render(request, 'academy/add_student.html', {'add_student_form': add_student_form,
                                                        'action_name': action_name
                                                        })


def add_lecturer(request):
    action_name = "Add lecturer"
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
        'message': message,
        'action_name': action_name
    }

    return render(request, 'academy/add_lecturer.html', context)


def del_lecturer(request, lecturer_id: int):
    lecturer = get_object_or_404(Lecturer, teacher_id=lecturer_id)
    lecturer.delete()
    return redirect('lecturers')


def edit_lecturer(request, lecturer_id: int):
    action_name = "Edit lecturer"
    lecturer = get_object_or_404(Lecturer, teacher_id=lecturer_id)
    if request.method == 'POST':
        add_lecturer_form = AddLecturerForm(request.POST, instance=lecturer)
        if add_lecturer_form.is_valid():
            lecturer = add_lecturer_form.save()
            lecturer.save()
            return redirect('lecturers')
    add_lecturer_form = AddLecturerForm(instance=lecturer)
    return render(request, 'academy/add_lecturer.html', {'add_lecturer_form': add_lecturer_form,
                                                         'action_name': action_name
                                                         })


def add_group(request):
    action_name = "Add group"
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
        'message': message,
        'action_name': action_name
    }

    return render(request, 'academy/add_group.html', context)


def del_group(request, group_id: int):
    group = get_object_or_404(Group, group=group_id)
    group.delete()
    return redirect('groups')


def edit_group(request, group_id: int):
    action_name = "Edit group"
    group = get_object_or_404(Group, group=group_id)
    if request.method == 'POST':
        add_group_form = AddGroupForm(request.POST, instance=group)
        if add_group_form.is_valid():
            group = add_group_form.save()
            group.save()
            return redirect('groups')
    add_group_form = AddGroupForm(instance=group)
    return render(request, 'academy/add_group.html', {'add_group_form': add_group_form,
                                                      'action_name': action_name
                                                      })
