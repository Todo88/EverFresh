# Generated by Django 2.0.1 on 2018-11-19 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freshsheet', '0037_auto_20181119_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='qb_customer_id',
            field=models.CharField(default='', max_length=20, verbose_name='Quickbooks ID Number'),
        ),
    ]
