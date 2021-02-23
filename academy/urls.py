from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_index),
    path('students', views.get_students, name='students'),
    path('lecturers', views.get_lecturers, name='lecturers'),
    path('groups', views.get_groups, name='groups'),
    path('addstudent', views.add_student),
    path('addgroup', views.add_group),
    path('addlecturer', views.add_lecturer),
    path('students/add/', views.add_student, name='add_student'),
    path('students/edit/<int:student_id>', views.edit_student, name='edit_student'),
    path('students/delete/<int:student_id>', views.del_student, name='delete_student'),
    path('lecturers/add/', views.add_lecturer, name='add_lecturer'),
    path('lecturers/edit/<int:lecturer_id>', views.edit_lecturer, name='edit_lecturer'),
    path('lecturers/delete/<int:lecturer_id>', views.del_lecturer, name='delete_lecturer'),
    path('groups/add/', views.add_group, name='add_group'),
    path('groups/edit/<int:group_id>', views.edit_group, name='edit_group'),
    path('groups/delete/<int:group_id>', views.del_group, name='delete_group'),
    path('contact', views.send_contact, name='contact')
]
