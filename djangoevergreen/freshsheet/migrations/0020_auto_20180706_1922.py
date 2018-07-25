# Generated by Django 2.0.1 on 2018-07-06 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('freshsheet', '0019_auto_20180704_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='unit',
            field=models.CharField(default='lb', max_length=15),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='freshsheet.FoodItem'),
        ),
    ]