# Generated by Django 5.1.3 on 2024-11-09 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='confirmed',
        ),
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=10),
        ),
        migrations.AddField(
            model_name='appointment',
            name='zoom_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
