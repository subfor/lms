from random import choice, randint

from academy.models import Group, Lecturer, Student

from django.core.management.base import BaseCommand

from faker import Faker


class Command(BaseCommand):
    """Adding 2 groups, 10 students and 1 lecturer in academy"""
    help = "Adding 2 groups, 10 students and 1 lecturer in academy"

    def handle(self, *args, **kwargs):
        fake = Faker("ru_RU")
        course_list = (
            "Python",
            "Python Adv",
            "Java",
            "Java Adv",
            "C",
            "C++",
            "C#",
            "PHP",
            "PHP Adv",
            "FrontEnd",
            "BackEnd",
            "DevOps",
        )
        for _ in range(2):
            course = choice(course_list)
            group_name = f"Group_{randint(1, 9999)}"
            group = Group.objects.create(course=course, group_name=group_name)
            lecturer = Lecturer.objects.create(first_name=fake.unique.first_name(),
                                               last_name=fake.unique.last_name(),
                                               email=fake.ascii_free_email()
                                               )
            lecturer.save()
            group.teachers.add(lecturer)
            for _ in range(10):
                student = Student.objects.create(first_name=fake.unique.first_name(),
                                                 last_name=fake.unique.last_name(),
                                                 email=fake.ascii_free_email()
                                                 )

                student.save()
                group.students.add(student)
            group.save()
