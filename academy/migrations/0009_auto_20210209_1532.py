# Generated by Django 3.1.6 on 2021-02-09 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0008_auto_20210209_1527'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='teacher',
            new_name='teachers',
        ),
    ]
