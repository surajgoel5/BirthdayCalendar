# Generated by Django 2.2.16 on 2020-09-04 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0002_auto_20200905_0216'),
    ]

    operations = [
        migrations.AddField(
            model_name='birthday',
            name='priority',
            field=models.IntegerField(choices=[(1, 'FAM'), (2, 'VVIP'), (3, 'VIP'), (4, 'GEN')], default=4),
        ),
    ]