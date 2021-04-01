from academy.models import Group, Lecturer, Student

from django.test import TestCase
from django.urls import reverse


class StudentListViewTest(TestCase):
    NUMBER_OF_STUDENT = 10

    @classmethod
    def setUpTestData(cls):
        cls.first_name = "Jhon"
        cls.last_name = "Doe"
        cls.email = "jdoe@fdsdf.com"
        cls.photo = "photo/default.png"

        for _ in range(cls.NUMBER_OF_STUDENT):
            cls.student = Student.objects.create(first_name=cls.first_name,
                                                 last_name=cls.last_name,
                                                 email=cls.email,
                                                 photo=cls.photo
                                                 )

    def test_view_students_url_exists_at_desired_location(self):
        resp = self.client.get('/students')
        self.assertEqual(resp.status_code, 200)

    def test_view_students_url_accessible_by_name(self):
        resp = self.client.get(reverse('students'))
        self.assertEqual(resp.status_code, 200)

    def test_lists_all_students(self):
        resp = self.client.get(reverse('students'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['students']) == self.NUMBER_OF_STUDENT)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('students'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'academy/students.html')


class LecturerListViewTest(TestCase):
    NUMBER_OF_LECTURERS = 10

    @classmethod
    def setUpTestData(cls):
        cls.first_name = "Jhon"
        cls.last_name = "Doe"
        cls.email = "jdoe@fdsdf.com"
        cls.photo = "photo/default.png"

        for _ in range(cls.NUMBER_OF_LECTURERS):
            cls.lecturer = Lecturer.objects.create(first_name=cls.first_name,
                                                   last_name=cls.last_name,
                                                   email=cls.email,
                                                   photo=cls.photo,
                                                   )

    def test_view_lecturers_url_exists_at_desired_location(self):
        resp = self.client.get('/lecturers')
        self.assertEqual(resp.status_code, 200)

    def test_view_lecturers_url_accessible_by_name(self):
        resp = self.client.get(reverse('lecturers'))
        self.assertEqual(resp.status_code, 200)

    def test_lists_all_lecturers(self):
        resp = self.client.get(reverse('lecturers'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['lecturers']) == self.NUMBER_OF_LECTURERS)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('lecturers'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'academy/lecturers.html')


class GroupListViewTest(TestCase):
    NUMBER_OF_STUDENT = 10
    NUMBER_OF_GROUP = 10

    @classmethod
    def setUpTestData(cls):
        cls.first_name = "Jhon"
        cls.last_name = "Doe"
        cls.email = "jdoe@fdsdf.com"
        cls.photo = "photo/default.png"

        for number in range(cls.NUMBER_OF_GROUP):
            group = Group.objects.create(course="Python",
                                         group_name=f"test_group{number}"
                                         )
            lecturer = Lecturer.objects.create(first_name=cls.first_name,
                                               last_name=cls.last_name,
                                               email=cls.email,
                                               photo=cls.photo,
                                               )
            group.teachers.add(lecturer)
            for _ in range(cls.NUMBER_OF_STUDENT):
                student = Student.objects.create(first_name=cls.first_name,
                                                 last_name=cls.last_name,
                                                 email=cls.email,
                                                 photo=cls.photo
                                                 )
                group.students.add(student)

    def test_view_groups_url_exists_at_desired_location(self):
        resp = self.client.get('/groups')
        self.assertEqual(resp.status_code, 200)

    def test_view_groups_url_accessible_by_name(self):
        resp = self.client.get(reverse('groups'))
        self.assertEqual(resp.status_code, 200)

    def test_lists_all_groups(self):
        resp = self.client.get(reverse('groups'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['groups']) == self.NUMBER_OF_GROUP)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('groups'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'academy/groups.html')
