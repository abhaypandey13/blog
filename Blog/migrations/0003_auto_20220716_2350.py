# Generated by Django 3.2.5 on 2022-07-16 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_alter_user_dob'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='user',
            name='lastname',
        ),
    ]
