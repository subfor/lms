from rest_framework.serializers import ModelSerializer

from academy.models import Group, Lecturer, Student


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ('student', 'first_name', 'last_name', 'email', 'photo')


class LecturerSerializer(ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ('teacher_id', 'first_name', 'last_name', 'email', 'photo')


class GroupSerializer(ModelSerializer):
    students = StudentSerializer(many=True, read_only=False)
    teachers = LecturerSerializer(many=True, read_only=False)

    class Meta:
        model = Group
        fields = ('group', 'course', 'students', 'teachers', 'group_name')
