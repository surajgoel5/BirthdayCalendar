# Generated by Django 2.2.16 on 2020-09-07 23:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0002_auto_20200908_0511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailedlist',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
