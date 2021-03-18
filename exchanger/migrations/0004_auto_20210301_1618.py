# Generated by Django 3.1.6 on 2021-03-01 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchanger', '0003_auto_20210301_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangerate',
            name='buy',
            field=models.DecimalField(decimal_places=3, max_digits=8),
        ),
        migrations.AlterField(
            model_name='exchangerate',
            name='sell',
            field=models.DecimalField(decimal_places=3, max_digits=8),
        ),
    ]