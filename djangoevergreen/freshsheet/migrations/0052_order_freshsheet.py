# Generated by Django 2.0.10 on 2019-01-28 22:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('freshsheet', '0051_remove_order_freshsheet'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='freshsheet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='freshsheet.FreshSheet'),
        ),
    ]
