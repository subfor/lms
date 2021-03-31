from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from academy.models import Group, Lecturer, Student


class StudentListViewTest(TestCase):
    NUMBER_OF_STUDENT = 10
    NUMBER_OF_GROUP = 10

    @classmethod
    def setUpTestData(cls):
        cls.first_name = "Jhon"
        cls.last_name = "Doe"
        cls.email = "jdoe@fdsdf.com"
        cls.photo = "photo/default.png"
        cls.lecturer = Lecturer.objects.create(first_name=cls.first_name,
                                               last_name=cls.last_name,
                                               email=cls.email,
                                               photo=cls.photo,
                                               )
        cls.student = Student.objects.create(first_name=cls.first_name,
                                             last_name=cls.last_name,
                                             email=cls.email,
                                             photo=cls.photo
                                             )
        for number in range(cls.NUMBER_OF_GROUP):
            group = Group.objects.create(course="Python",
                                         group_name=f"test_group{number}"
                                         )
            group.teachers.add(cls.lecturer)
            for _ in range(cls.NUMBER_OF_STUDENT):
                group.students.add(cls.student)

    def test_view_students_url_exists_at_desired_location(self):
        resp = self.client.get('/students')
        self.assertEqual(resp.status_code, 200)

    def test_view_students_url_accessible_by_name(self):
        resp = self.client.get(reverse('students'))
        self.assertEqual(resp.status_code, 200)

    def test_lists_all_students(self):
        resp = self.client.get(reverse('students'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['students']) == 100)
