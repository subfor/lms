# Generated by Django 3.1.6 on 2021-02-09 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='teacher',
        ),
        migrations.AddField(
            model_name='group',
            name='teacher',
            field=models.ManyToManyField(to='academy.Lecturer'),
        ),
    ]
