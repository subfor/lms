from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, FormView, UpdateView, DeleteView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK

from LMS.settings import STUDENTS_PER_PAGE, LECTURERS_PER_PAGE, GROUPS_PER_PAGE
from academy.forms import AddGroupForm, AddLecturerForm, AddStudentForm, ContactForm
from academy.models import Group, Lecturer, Student
from academy.serializers import StudentSerializer, GroupSerializer
from academy.tasks import send_mail

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from exchanger.models import ExchangeRate


def get_index(request):
    rates = ExchangeRate.objects.all()
    if rates.exists():
        return render(request, 'academy/start.html', {'rates': rates.values()})
    return render(request, 'academy/start.html')


def get_students(request):
    students = Student.objects.all().order_by('-student')
    paginator = Paginator(students, STUDENTS_PER_PAGE)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
    return render(request, 'academy/students.html', {'students': students, 'page': page})


def get_lecturers(request):
    lecturers = Lecturer.objects.all().order_by('-teacher_id')
    paginator = Paginator(lecturers, LECTURERS_PER_PAGE)
    page = request.GET.get('page')
    try:
        lecturers = paginator.page(page)
    except PageNotAnInteger:
        lecturers = paginator.page(1)
    except EmptyPage:
        lecturers = paginator.page(paginator.num_pages)
    return render(request, 'academy/lecturers.html', {'lecturers': lecturers, 'page': page})


def get_groups(request):
    groups = Group.objects.all().order_by('-group')
    paginator = Paginator(groups, GROUPS_PER_PAGE)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)
    return render(request, 'academy/groups.html', {'groups': groups, 'page': page})


@user_passes_test(lambda user: user.is_staff)
def add_student(request):
    action_name = "Add student"
    student = None
    message = ""
    if request.method == 'POST':
        add_student_form = AddStudentForm(data=request.POST)
        if add_student_form.is_valid():
            student = add_student_form.save()
            # bez etogo signal ne rabotaet i s etim commit=False spisok ne pashet
            student.save()
            message = f"Student {student.first_name} {student.last_name} successfully added to LMS"
    context = {
        'student': student,
        'add_student_form': AddStudentForm(),
        'message': message,
        'action_name': action_name
    }

    return render(request, 'academy/add_student.html', context)


@user_passes_test(lambda user: user.is_staff)
def del_student(request, student_id: int):
    student = get_object_or_404(Student, student=student_id)
    student.delete()
    return redirect('students')


@user_passes_test(lambda user: user.is_staff)
# @cache_page(60 * 5)
def edit_student(request, student_id: int):
    action_name = "Edit student"
    student = get_object_or_404(Student, student=student_id)
    if request.method == 'POST':
        add_student_form = AddStudentForm(request.POST, instance=student)
        if add_student_form.is_valid():
            # vopros sprosit'
            student = add_student_form.save()
            student.save()
            return redirect('students')
    add_student_form = AddStudentForm(instance=student)
    return render(request, 'academy/add_student.html', {'add_student_form': add_student_form,
                                                        'action_name': action_name
                                                        })


@user_passes_test(lambda user: user.is_staff)
def add_lecturer(request):
    action_name = "Add lecturer"
    lecturer = None
    message = ""
    if request.method == 'POST':
        add_lecturer_form = AddLecturerForm(data=request.POST)
        if add_lecturer_form.is_valid():
            lecturer = add_lecturer_form.save()
            lecturer.save()
            message = f"Lecturer {lecturer.first_name} {lecturer.last_name} successfully added to LMS"
    context = {
        'lecturer': lecturer,
        'add_lecturer_form': AddLecturerForm(),
        'message': message,
        'action_name': action_name
    }

    return render(request, 'academy/add_lecturer.html', context)


@user_passes_test(lambda user: user.is_staff)
def del_lecturer(request, lecturer_id: int):
    lecturer = get_object_or_404(Lecturer, teacher_id=lecturer_id)
    lecturer.delete()
    return redirect('lecturers')


@user_passes_test(lambda user: user.is_staff)
# @cache_page(60 * 5)
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


@user_passes_test(lambda user: user.is_staff)
def add_group(request):
    action_name = "Add group"
    group = None
    message = ""
    if request.method == 'POST':
        add_group_form = AddGroupForm(data=request.POST)
        if add_group_form.is_valid():
            group = add_group_form.save()
            group.save()
            message = f"Group {group.group_name} successfully added to LMS"

    context = {
        'group': group,
        'add_group_form': AddGroupForm(),
        'message': message,
        'action_name': action_name
    }

    return render(request, 'academy/add_group.html', context)


@user_passes_test(lambda user: user.is_staff)
def del_group(request, group_id: int):
    group = get_object_or_404(Group, group=group_id)
    group.delete()
    return redirect('groups')


@user_passes_test(lambda user: user.is_staff)
# @cache_page(60 * 5)
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


def send_contact(request):
    message = ""
    if request.method == 'POST':
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            sent = request.session.get('sent')
            if sent:
                message = f"We are get your message, please try again after{request.session.get_expiry_age()} seconds"
                contact_form = ContactForm()
            else:
                request.session.set_expiry(timedelta(seconds=180))
                message = "Message sent"
                send_mail.delay(contact_form.cleaned_data)
                contact_form = ContactForm()
                request.session['sent'] = True
                request.session.modified = True

            return render(request, 'academy/contact.html', {'contact_form': contact_form,
                                                            'message': message
                                                            })
        else:
            return render(request, 'academy/contact.html', {'contact_form': contact_form})
    else:
        contact_form = ContactForm()
    return render(request, 'academy/contact.html', {'contact_form': contact_form})


# class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
#
#     def test_func(self):
#         return self.request.user.is_superuser or self.request.user.is_staff


class StudentsCreateView(ListView):
    model = Student
    ordering = ['-student']
    template_name = 'academy/students_new.html'
    fields = ['student', 'photo', 'first_name', 'last_name', 'email']


class StudentsAddView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Student
    template_name = 'academy/add_student_new.html'
    fields = ['first_name', 'last_name', 'email', 'photo']
    success_message = "Student successfully added"
    success_url = reverse_lazy('add_student_new')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class StudentsEditView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Student
    template_name = 'academy/add_student_new.html'
    fields = ['first_name', 'last_name', 'email', 'photo']
    success_message = "Student successfully edit"

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_success_url(self, **kwargs):
        return reverse("edit_student_new", kwargs={'pk': self.object.pk})


class StudentsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('students_new')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class LecturersCreateView(ListView):
    model = Lecturer
    ordering = ['-teacher_id']
    template_name = 'academy/lecturers_new.html'
    fields = ['teacher_id', 'photo', 'first_name', 'last_name', 'email']


class LecturersAddView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Lecturer
    template_name = 'academy/add_lecturer_new.html'
    fields = ['first_name', 'last_name', 'email', 'photo']
    success_message = "Lecturer successfully added"
    success_url = reverse_lazy('add_lecturer_new')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class LecturersEditView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Lecturer
    template_name = 'academy/add_lecturer_new.html'
    fields = ['first_name', 'last_name', 'email', 'photo']
    success_message = "Lecturer successfully edit"

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_success_url(self, **kwargs):
        return reverse("edit_lecturer_new", kwargs={'pk': self.object.pk})


class LecturersDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Lecturer
    success_url = reverse_lazy('lecturers_new')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def students(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        rdata = request.data
        data = {
            'first_name': rdata.get('first_name'),
            'last_name': rdata.get('last_name'),
            'email': rdata.get('email'),
        }
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def student(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    if request.method == 'DELETE':
        student.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        first_name = request.data.get('first_name')
        if first_name:
            student.first_name = first_name
        last_name = request.data.get('last_name')
        if last_name:
            student.last_name = last_name
        email = request.data.get('email')
        if email:
            student.email = email
        student.save()
        return Response(status=HTTP_200_OK)


"""
asd
"""


# ields = ('group', 'course', 'students', 'teachers', 'group_name')

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def groups(request):
    if request.method == 'GET':
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        rdata = request.data
        data = {
            'course': rdata.get('course'),
            'group_name': rdata.get('group_name'),
            'students': rdata.get('students'),
            'teachers': rdata.get('teachers'),
        }
        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def group(request, group_id):
    try:
        group = Group.objects.get(pk=group_id)
    except Group.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    if request.method == 'DELETE':
        group.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        course = request.data.get('course')
        if course:
            group.course = course

        group_name = request.data.get('group_name')
        if group_name:
            group.group_name = group_name

        students = request.data.get('students')
        if students:
            for existing_student in group.students.all():
                group.students.remove(existing_student)
            for student in students:
                group.students.add(student)

        teachers = request.data.get('teachers')
        if teachers:
            for existing_teachers in group.teachers.all():
                group.teachers.remove(existing_teachers)
            for teacher in teachers:
                group.teachers.add(teacher)
        group.save()
        return Response(status=HTTP_200_OK)
