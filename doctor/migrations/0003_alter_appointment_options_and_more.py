# Generated by Django 4.1.6 on 2023-11-28 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_alter_appointment_accepted_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'ordering': ['-sent_date']},
        ),
        migrations.RenameField(
            model_name='appointment',
            old_name='send_date',
            new_name='sent_date',
        ),
    ]
