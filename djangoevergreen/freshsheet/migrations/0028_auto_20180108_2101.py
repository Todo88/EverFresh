# Generated by Django 2.0.1 on 2018-01-08 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freshsheet', '0027_auto_20180108_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='vegetables/'),
        ),
    ]
