# Generated by Django 3.1.6 on 2021-02-09 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0003_student_groups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='groups',
        ),
    ]
