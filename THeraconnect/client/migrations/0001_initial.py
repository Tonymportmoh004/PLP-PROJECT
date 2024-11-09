# Generated by Django 5.1.3 on 2024-11-09 15:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('confirmed', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to=settings.AUTH_USER_MODEL)),
                ('therapist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='therapist_appointments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date', 'start_time'],
                'indexes': [models.Index(fields=['therapist', 'date', 'start_time', 'end_time'], name='client_appo_therapi_4b8c4f_idx')],
                'unique_together': {('client', 'therapist', 'date', 'start_time', 'end_time')},
            },
        ),
    ]