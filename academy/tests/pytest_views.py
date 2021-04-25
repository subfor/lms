from academy.models import Group, Lecturer, Student
from academy.tests.factory import UserFactory

from django.urls import reverse

import pytest

NUMBER_OF_LECTURERS = 10
NUMBER_OF_STUDENTS = 10
NUMBER_OF_GROUPS = 10


@pytest.fixture
def create_user(django_user_model):
    def make_user(**kwargs):
        return UserFactory.create(**kwargs)

    return make_user


"""
Tests lecturers
"""


@pytest.fixture
def lecturer():
    return Lecturer.objects.create(first_name="Jhon",
                                   last_name="Doe",
                                   email="jdoe@fdsdf.com",
                                   photo="photo/default.png",
                                   )


@pytest.fixture
def create_lecturers():
    def make_lecturers(**kwargs):
        # author = kwargs['author'] if 'author' in kwargs else user
        number_of_lecturers = kwargs['number_of_lecturers']
        lecturers = []
        for _ in range(number_of_lecturers):
            lecturer = Lecturer.objects.create(first_name="Jhon",
                                               last_name="Doe",
                                               email="jdoe@fdsdf.com",
                                               photo="photo/default.png",
                                               )
            lecturers.append(lecturer)
        return lecturers

    return make_lecturers


@pytest.mark.django_db
def test_view_lecturers_url_exists_at_desired_location(client):
    resp = client.get('/lecturers')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_view_lecturers_url_accessible_by_name(client):
    resp = client.get(reverse('lecturers'))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_lists_one_lecturer(client, lecturer):
    resp = client.get(reverse('lecturers'))
    assert resp.status_code == 200
    assert len(resp.context['lecturers']) == 1


@pytest.mark.django_db
def test_lists_all_lecturers(client, create_lecturers):
    create_lecturers(number_of_lecturers=NUMBER_OF_LECTURERS)
    resp = client.get(reverse('lecturers'))
    assert resp.status_code == 200
    assert len(resp.context['lecturers']) == NUMBER_OF_LECTURERS


@pytest.mark.django_db
def test_view_uses_lecturers_correct_template(client):
    resp = client.get(reverse('lecturers'))
    assert resp.status_code == 200
    assert 'academy/lecturers.html' in (templ.name for templ in resp.templates)


"""
Tests students
"""


@pytest.fixture
def student():
    return Student.objects.create(first_name="Jhon",
                                  last_name="Doe",
                                  email="jdoe@fdsdf.com",
                                  photo="photo/default.png",
                                  )


@pytest.fixture
def create_students():
    def make_students(**kwargs):
        number_of_students = kwargs['number_of_students']
        students = []
        for _ in range(number_of_students):
            student = Student.objects.create(first_name="Jhon",
                                             last_name="Doe",
                                             email="jdoe@fdsdf.com",
                                             photo="photo/default.png",
                                             )
            students.append(student)
        return students

    return make_students


@pytest.mark.django_db
def test_view_students_url_exists_at_desired_location(client):
    resp = client.get('/students')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_view_students_url_accessible_by_name(client):
    resp = client.get(reverse('students'))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_lists_one_student(client, student):
    resp = client.get(reverse('students'))
    assert resp.status_code == 200
    assert len(resp.context['students']) == 1


@pytest.mark.django_db
def test_lists_all_students(client, create_students):
    create_students(number_of_students=NUMBER_OF_STUDENTS)
    resp = client.get(reverse('students'))
    assert resp.status_code == 200
    assert len(resp.context['students']) == NUMBER_OF_STUDENTS


@pytest.mark.django_db
def test_view_uses_students_correct_template(client):
    resp = client.get(reverse('students'))
    assert resp.status_code == 200
    assert 'academy/students.html' in (templ.name for templ in resp.templates)


"""
Tests groups
"""


@pytest.fixture
def group_create(lecturer, student):
    group = Group.objects.create(course="Python",
                                 group_name="test_group"
                                 )
    for _ in range(NUMBER_OF_STUDENTS):
        group.students.add(student)
    group.teachers.add(lecturer)

    return group


@pytest.fixture
def create_groups(lecturer, student):
    def make_groups(**kwargs):
        number_of_groups = kwargs['number_of_groups']
        groups = []
        for number in range(number_of_groups):
            group = Group.objects.create(course="Python",
                                         group_name=f"test_group{number}"
                                         )
            group.teachers.add(lecturer)
            for _ in range(NUMBER_OF_STUDENTS):
                group.students.add(student)
        return groups

    return make_groups


@pytest.mark.django_db
def test_lists_one_group(client, group_create):
    resp = client.get(reverse('groups'))
    assert resp.status_code == 200
    assert len(resp.context['groups']) == 1


@pytest.mark.django_db
def test_lists_all_groups(client, create_groups):
    create_groups(number_of_groups=NUMBER_OF_GROUPS)
    resp = client.get(reverse('groups'))
    assert resp.status_code == 200
    assert len(resp.context['groups']) == NUMBER_OF_GROUPS


@pytest.mark.django_db
def test_view_groups_url_exists_at_desired_location(client):
    resp = client.get('/groups')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_view_groups_url_accessible_by_name(client):
    resp = client.get(reverse('groups'))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_view_uses_groups_correct_template(client):
    resp = client.get(reverse('groups'))
    assert resp.status_code == 200
    assert 'academy/groups.html' in (templ.name for templ in resp.templates)


"""
Tests buttons in menu
"""


@pytest.mark.django_db
def test_hide_add_buttons_for_not_authenticated_user_in_menu(client):
    resp = client.get(reverse('index'))
    assert resp.status_code == 200
    expected_link_add_student = '<a class="py-2 d-none d-md-inline-block" href="/addstudent">'
    expected_link_add_lecturer = '<a class="py-2 d-none d-md-inline-block" href="/addlecturer">'
    expected_link_add_group = '<a class="py-2 d-none d-md-inline-block" href="/addgroup">'
    assert expected_link_add_student.encode() not in resp.content
    assert expected_link_add_lecturer.encode() not in resp.content
    assert expected_link_add_group.encode() not in resp.content


@pytest.mark.django_db
def test_hide_add_buttons_for_authenticated_not_staff_users_in_menu(client, create_user):
    user = create_user()
    client.force_login(user)
    resp = client.get(reverse('index'))
    assert resp.status_code == 200
    expected_link_add_student = '<a class="py-2 d-none d-md-inline-block" href="/addstudent">'
    expected_link_add_lecturer = '<a class="py-2 d-none d-md-inline-block" href="/addlecturer">'
    expected_link_add_group = '<a class="py-2 d-none d-md-inline-block" href="/addgroup">'
    assert expected_link_add_student.encode() not in resp.content
    assert expected_link_add_lecturer.encode() not in resp.content
    assert expected_link_add_group.encode() not in resp.content


@pytest.mark.django_db
def test_show_add_buttons_for_authenticated_staff_users_in_menu(client, create_user):
    user = create_user(is_staff='True')
    client.force_login(user)
    resp = client.get(reverse('index'))
    assert resp.status_code == 200
    expected_link_add_student = '<a class="py-2 d-none d-md-inline-block" href="/addstudent">'
    expected_link_add_lecturer = '<a class="py-2 d-none d-md-inline-block" href="/addlecturer">'
    expected_link_add_group = '<a class="py-2 d-none d-md-inline-block" href="/addgroup">'
    assert expected_link_add_student.encode() in resp.content
    assert expected_link_add_lecturer.encode() in resp.content
    assert expected_link_add_group.encode() in resp.content


"""
Test create user button in students
"""


@pytest.mark.django_db
def test_show_add_student_buttons_for_authenticated_staff_users(client, create_user):
    user = create_user(is_staff='True')
    client.force_login(user)
    resp = client.get(reverse('students'))
    assert resp.status_code == 200
    expected_link_add_student = '<a href="students/add">'
    assert expected_link_add_student.encode() in resp.content


@pytest.mark.django_db
def test_show_add_student_buttons_for_authenticated_users(client, create_user):
    user = create_user()
    client.force_login(user)
    resp = client.get(reverse('students'))
    assert resp.status_code == 200
    expected_link_add_student = '<a href="students/add">'
    assert expected_link_add_student.encode() not in resp.content


@pytest.mark.django_db
def test_show_add_student_buttons_for_not_authenticated_users(client):
    resp = client.get(reverse('students'))
    assert resp.status_code == 200
    expected_link_add_student = '<a href="students/add">'
    assert expected_link_add_student.encode() not in resp.content


"""
Test create user button in lecturers
"""


@pytest.mark.django_db
def test_show_add_lecturer_buttons_for_authenticated_staff_users(client, create_user):
    user = create_user(is_staff='True')
    client.force_login(user)
    resp = client.get(reverse('lecturers'))
    assert resp.status_code == 200
    expected_link_add_lecturer = '<a href="lecturers/add">'
    assert expected_link_add_lecturer.encode() in resp.content


@pytest.mark.django_db
def test_show_add_lecturer_buttons_for_authenticated_users(client, create_user):
    user = create_user()
    client.force_login(user)
    resp = client.get(reverse('lecturers'))
    assert resp.status_code == 200
    expected_link_add_lecturer = '<a href="lecturers/add">'
    assert expected_link_add_lecturer.encode() not in resp.content


@pytest.mark.django_db
def test_show_add_lecturer_buttons_for_not_authenticated_users(client):
    resp = client.get(reverse('lecturers'))
    assert resp.status_code == 200
    expected_link_add_lecturer = '<a href="lecturers/add">'
    assert expected_link_add_lecturer.encode() not in resp.content
