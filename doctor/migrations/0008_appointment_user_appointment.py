# Generated by Django 4.1.6 on 2023-12-01 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doctor', '0007_appointment_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='user_appointment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]