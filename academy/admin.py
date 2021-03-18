import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Group, Lecturer, Student

admin.site.register(Group)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    actions = ['export']

    def export(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="students.csv"'
        writer = csv.writer(response)
        header = ['FirstName', 'LastName', 'Email']
        writer.writerow(header)
        for person in queryset:
            row = [
                person.first_name,
                person.last_name,
                person.email
            ]
            writer.writerow(row)
        return response

    export.short_description = 'Export students'


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    actions = ['export']

    def export(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="lecturers.csv"'
        writer = csv.writer(response)
        header = ['FirstName', 'LastName', 'Email']
        writer.writerow(header)
        for person in queryset:
            row = [
                person.first_name,
                person.last_name,
                person.email
            ]
            writer.writerow(row)
        return response

    export.short_description = 'Export lecturers'
# Register your models here.
