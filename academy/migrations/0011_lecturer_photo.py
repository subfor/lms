# Generated by Django 3.1.6 on 2021-03-17 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0010_student_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturer',
            name='photo',
            field=models.ImageField(default='photo/default.png', upload_to='photo/'),
        ),
    ]
