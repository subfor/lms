from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from academy.models import Group, Lecturer, Student
from django.test import TestCase


class StudentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.first_name = "Jhon"
        cls.last_name = "Doe"
        cls.email = "jdoe@fdsdf.com"
        cls.photo = "photo/default.png"
        cls.lecturer = Lecturer.objects.create(first_name=cls.first_name,
                                               last_name=cls.last_name,
                                               email=cls.email,
                                               photo=cls.photo
                                               )
        cls.lecturer.save()
        cls.student = Student.objects.create(first_name=cls.first_name,
                                             last_name=cls.last_name,
                                             email=cls.email,
                                             photo=cls.photo
                                             )
        cls.lecturer.save()

    def setUp(self) -> None:
        # вызывается перед каждой тестовой функцией для настройки объектов,
        # которые могут изменяться во время тестов
        pass

    def tearDown(self) -> None:
        pass

    def test_successfully_student_creation(self):
        student = Student(first_name=self.first_name,
                          last_name=self.last_name,
                          email=self.email,
                          photo=self.photo
                          )
        student.full_clean()

    def test_successfully_lecturer_creation(self):
        student = Lecturer(first_name=self.first_name,
                           last_name=self.last_name,
                           email=self.email,
                           photo=self.photo
                           )
        student.full_clean()

    def test_successfully_group_creation(self):
        group = Group(course="Python",
                      group_name="test_group"
                      )

        group.teachers.add(self.lecturer)

        group.students.add(self.student)

        # # group.save()
        group.full_clean()

    # def test_successfully_group_creation(self):
    #     group = Group(course="Python",
    #                   group_name="test_group"
    #                   )
    #     lecturer = Lecturer.objects.create(first_name=self.first_name,
    #                                        last_name=self.last_name,
    #                                        email=self.email,
    #                                        photo=self.photo
    #                                        )
    #     lecturer.save()
    #     group.teachers.add(lecturer)
    #     student = Student.objects.create(first_name=self.first_name,
    #                                      last_name=self.last_name,
    #                                      email=self.email,
    #                                      photo=self.photo
    #                                      )
    #
    #     student.save()
    #     group.students.add(student)
    #
    #     # # group.save()
    #     group.full_clean()
