# Generated by Django 4.1.6 on 2023-11-30 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0005_alter_appointment_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='time',
        ),
    ]
