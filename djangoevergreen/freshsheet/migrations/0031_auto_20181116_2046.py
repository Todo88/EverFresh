# Generated by Django 2.0.1 on 2018-11-16 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freshsheet', '0030_auto_20181116_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='qb_access_token',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
