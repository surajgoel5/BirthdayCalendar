# Generated by Django 2.2.16 on 2020-09-04 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Birthday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bday', models.DateTimeField(verbose_name='birthday')),
                ('fblink', models.CharField(max_length=100)),
            ],
        ),
    ]