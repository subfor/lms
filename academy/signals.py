from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Group, Lecturer, Student


# @receiver(post_save)
@receiver(post_save, sender=Group)
@receiver(post_save, sender=Lecturer)
@receiver(post_save, sender=Student)
def capitalize_names_groups(sender, instance, **kwargs):
    if sender.__name__ == 'Group':
        instance.group_name = instance.group_name.capitalize()
        instance.course = instance.course.capitalize()
    else:
        instance.first_name = instance.first_name.capitalize()
        instance.last_name = instance.last_name.capitalize()
