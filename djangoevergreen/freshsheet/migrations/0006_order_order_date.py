# Generated by Django 2.0.1 on 2018-02-09 17:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('freshsheet', '0005_auto_20180208_2318'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date'),
            preserve_default=False,
        ),
    ]