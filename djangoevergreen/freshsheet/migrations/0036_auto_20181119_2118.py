# Generated by Django 2.0.1 on 2018-11-19 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freshsheet', '0035_accountrequest_business_city_st_zip'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountrequest',
            name='business_state',
            field=models.CharField(default='', max_length=15, verbose_name='State'),
        ),
        migrations.AddField(
            model_name='accountrequest',
            name='business_zipcode',
            field=models.CharField(default='', max_length=15, verbose_name='Zip Code'),
        ),
        migrations.AlterField(
            model_name='accountrequest',
            name='business_city_st_zip',
            field=models.CharField(default='', max_length=25, verbose_name='City'),
        ),
    ]
