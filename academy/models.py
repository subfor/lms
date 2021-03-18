from django.db import models


class Student(models.Model):
    student = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30, verbose_name='Name')
    last_name = models.CharField(max_length=30, verbose_name='Last Name')
    email = models.EmailField(max_length=50, verbose_name='Email')
    photo = models.ImageField(upload_to='photo/', default='photo/default.png')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Lecturer(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30, verbose_name='Name')
    last_name = models.CharField(max_length=30, verbose_name='Last Name')
    email = models.EmailField(max_length=50, verbose_name='Email')
    photo = models.ImageField(upload_to='photo/', default='photo/default.png')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Group(models.Model):
    group = models.AutoField(primary_key=True)
    course = models.CharField(max_length=30)
    students = models.ManyToManyField(Student, verbose_name="Students")
    teachers = models.ManyToManyField(Lecturer)
    group_name = models.CharField(max_length=20, unique=True, verbose_name='Group')

    def __str__(self):
        return f"{self.group_name}"