from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_index),
    path('students', views.get_students),
    path('lecturers', views.get_lecturers),
    path('groups', views.get_groups)
]
