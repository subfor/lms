from academy.models import Group

from django import template


register = template.Library()


@register.filter()
def get_count_students(value):
    group = Group.objects.filter(group_name=value)[0]
    return f'{value} ({group.students.count()})'
