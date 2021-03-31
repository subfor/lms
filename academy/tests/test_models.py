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
                                               photo=cls.photo,
                                               )
        cls.student = Student.objects.create(first_name=cls.first_name,
                                             last_name=cls.last_name,
                                             email=cls.email,
                                             photo=cls.photo
                                             )

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

    def test_failure_due_to_student_long_first_name(self):
        long_first_name = 'a' * 31
        student = Student(first_name=long_first_name,
                          last_name=self.last_name,
                          email=self.email,
                          photo=self.photo
                          )
        expected_message = 'Ensure this value has at most 30 characters (it has 31).'
        with self.assertRaisesMessage(ValidationError, expected_message):
            student.full_clean()

    def test_failure_due_to_student_long_last_name(self):
        long_last_name = 'a' * 31
        student = Student(first_name=self.first_name,
                          last_name=long_last_name,
                          email=self.email,
                          photo=self.photo
                          )
        expected_message = 'Ensure this value has at most 30 characters (it has 31).'
        with self.assertRaisesMessage(ValidationError, expected_message):
            student.full_clean()

    def test_failure_due_to_student_long_valid_email(self):
        long_email = f"{'a' * 42}@mail.com"
        email = Student(first_name=self.first_name,
                        last_name=self.last_name,
                        email=long_email,
                        photo=self.photo
                        )
        expected_message = 'Ensure this value has at most 50 characters (it has 51).'
        with self.assertRaisesMessage(ValidationError, expected_message):
            email.full_clean()

    def test_failure_due_to_student_long_not_valid_email(self):
        long_email = 'a' * 51
        email = Student(first_name=self.first_name,
                        last_name=self.last_name,
                        email=long_email,
                        photo=self.photo
                        )
        expected_messages = 'Enter a valid email address.'
        with self.assertRaisesMessage(ValidationError, expected_messages):
            email.full_clean()

    def test_successfully_lecturer_creation(self):
        student = Lecturer(first_name=self.first_name,
                           last_name=self.last_name,
                           email=self.email,
                           photo=self.photo
                           )
        student.full_clean()

    def test_failure_due_to_lecturer_long_first_name(self):
        long_first_name = 'a' * 31
        lecturer = Lecturer(first_name=long_first_name,
                            last_name=self.last_name,
                            email=self.email,
                            photo=self.photo
                            )
        expected_message = 'Ensure this value has at most 30 characters (it has 31).'
        with self.assertRaisesMessage(ValidationError, expected_message):
            lecturer.full_clean()

    def test_failure_due_to_lecturer_long_last_name(self):
        long_last_name = 'a' * 31
        lecturer = Lecturer(first_name=self.first_name,
                            last_name=long_last_name,
                            email=self.email,
                            photo=self.photo
                            )
        expected_message = 'Ensure this value has at most 30 characters (it has 31).'
        with self.assertRaisesMessage(ValidationError, expected_message):
            lecturer.full_clean()

    def test_failure_due_to_lecturer_long_valid_email(self):
        long_email = f"{'a' * 42}@mail.com"
        email = Lecturer(first_name=self.first_name,
                         last_name=self.last_name,
                         email=long_email,
                         photo=self.photo
                         )
        expected_message = 'Ensure this value has at most 50 characters (it has 51).'
        with self.assertRaisesMessage(ValidationError, expected_message):
            email.full_clean()

    def test_failure_due_to_lecturer_long_not_valid_email(self):
        long_email = 'a' * 51
        email = Lecturer(first_name=self.first_name,
                         last_name=self.last_name,
                         email=long_email,
                         photo=self.photo
                         )
        expected_messages = 'Enter a valid email address.'
        with self.assertRaisesMessage(ValidationError, expected_messages):
            email.full_clean()

    def test_successfully_group_creation(self):
        group = Group.objects.create(course="Python",
                                     group_name="test_group"
                                     )
        group.teachers.add(self.lecturer)
        group.students.add(self.student)
        # validiruet ne sozdanie obekti
        # group.full_clean()

    def test_failure_due_to_group_long_course_field(self):
        long_course = 'a' * 31
        group = Group.objects.create(course=long_course,
                                     group_name="test_group"
                                     )

        expected_message = 'Ensure this value has at most 30 characters (it has 31).'
        with self.assertRaisesMessage(ValidationError, expected_message):
            group.full_clean()

    def test_failure_due_to_group_long_group_name(self):
        long_group_name = 'a' * 21
        group = Group.objects.create(course="Python",
                                     group_name=long_group_name
                                     )

        expected_message = 'Ensure this value has at most 20 characters (it has 21).'
        with self.assertRaisesMessage(ValidationError, expected_message):
            group.full_clean()