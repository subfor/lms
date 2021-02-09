from django.contrib import admin
from .models import Group, Student, Lecturer


admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Lecturer)

# Register your models here.
