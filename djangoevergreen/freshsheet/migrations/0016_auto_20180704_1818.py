# Generated by Django 2.0.1 on 2018-07-04 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freshsheet', '0015_auto_20180703_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='case_price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=5, null=True, verbose_name='Case Price'),
        ),
    ]
