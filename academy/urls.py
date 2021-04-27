from django.urls import path

from . import views
from .views import StudentsCreateView, StudentsAddView, StudentsEditView, StudentsDeleteView, LecturersCreateView, \
    LecturersAddView, LecturersDeleteView, LecturersEditView

urlpatterns = [
    path('', views.get_index, name='index'),
    path('students', views.get_students, name='students'),
    path('students/new/', StudentsCreateView.as_view(), name='students_new'),
    path('addstudent/new/', StudentsAddView.as_view(), name='add_student_new'),
    path('editstudent/new/<int:pk>/', StudentsEditView.as_view(), name='edit_student_new'),
    path('deletestudent/new/<int:pk>/', StudentsDeleteView.as_view(), name='delete_student_new'),
    path('lecturers', views.get_lecturers, name='lecturers'),
    path('lecturers/new/', LecturersCreateView.as_view(), name='lecturers_new'),
    path('addlecturer/new/', LecturersAddView.as_view(), name='add_lecturer_new'),
    path('editlecturer/new/<int:pk>/', LecturersEditView.as_view(), name='edit_lecturer_new'),
    path('deletelecturer/new/<int:pk>/', LecturersDeleteView.as_view(), name='delete_lecturer_new'),
    path('groups', views.get_groups, name='groups'),
    path('addstudent', views.add_student),
    path('addgroup', views.add_group),
    path('addlecturer', views.add_lecturer),
    path('students/add/', views.add_student, name='add_student'),
    path('students/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:student_id>/', views.del_student, name='delete_student'),
    path('lecturers/add/', views.add_lecturer, name='add_lecturer'),
    path('lecturers/edit/<int:lecturer_id>/', views.edit_lecturer, name='edit_lecturer'),
    path('lecturers/delete/<int:lecturer_id>/', views.del_lecturer, name='delete_lecturer'),
    path('groups/add/', views.add_group, name='add_group'),
    path('groups/edit/<int:group_id>/', views.edit_group, name='edit_group'),
    path('groups/delete/<int:group_id>/', views.del_group, name='delete_group'),
    path('contact', views.send_contact, name='contact')
]
