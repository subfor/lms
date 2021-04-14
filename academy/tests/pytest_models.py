from academy.models import Student

from django.core.exceptions import ValidationError

import pytest


@pytest.mark.django_db
def test_successfully_student_creation():
    first_name = "Jhon"
    last_name = "Doe"
    email = "jdoe@fdsdf.com"
    photo = "photo/default.png"

    Student(first_name=first_name,
            last_name=last_name,
            email=email,
            photo=photo
            ).save()
    assert Student.objects.count() == 1


@pytest.mark.django_db
def test_failure_due_to_student_long_first_name():
    long_first_name = 'a' * 31
    last_name = "Doe"
    email = "jdoe@fdsdf.com"
    photo = "photo/default.png"
    student = Student(first_name=long_first_name,
                      last_name=last_name,
                      email=email,
                      photo=photo
                      )

    # django.core.exceptions.ValidationError:
    # {'first_name': ['Ensure this value has at most 30 characters (it has 31).']}.
    with pytest.raises(ValidationError):
        student.full_clean()
    assert Student.objects.count() == 0
