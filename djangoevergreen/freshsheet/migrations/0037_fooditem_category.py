# Generated by Django 2.0.1 on 2018-01-10 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freshsheet', '0036_delete_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='category',
            field=models.CharField(blank=True, default='', max_length=40, null=True),
        ),
    ]
