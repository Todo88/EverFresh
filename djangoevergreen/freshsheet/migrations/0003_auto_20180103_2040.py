# Generated by Django 2.0.1 on 2018-01-03 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('freshsheet', '0002_auto_20180103_1915'),
    ]

    operations = [
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('phone', models.CharField(default='', max_length=15)),
                ('email', models.EmailField(default='', max_length=254)),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], default='WA', max_length=40, null=True)),
                ('city', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_name', models.CharField(default='', max_length=100)),
                ('phone', models.CharField(default='', max_length=15)),
                ('restaurant_name', models.CharField(default='', max_length=100)),
                ('email', models.EmailField(default='', max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Vegetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('inventory', models.PositiveIntegerField(default=0, max_length=1000000)),
                ('unit', models.CharField(default='', max_length=20)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vegetables', to='freshsheet.Farm')),
            ],
        ),
        migrations.RemoveField(
            model_name='freshsheet',
            name='farms',
        ),
        migrations.RemoveField(
            model_name='freshsheet',
            name='vegetable',
        ),
    ]
