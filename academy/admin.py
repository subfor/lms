from django.contrib import admin

from .models import Group, Lecturer, Student

admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Lecturer)

# Register your models here.
