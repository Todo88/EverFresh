# Generated by Django 2.0.1 on 2018-07-25 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freshsheet', '0023_user_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user',
        ),
    ]
