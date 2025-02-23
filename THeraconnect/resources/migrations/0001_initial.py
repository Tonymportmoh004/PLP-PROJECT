# Generated by Django 5.1.3 on 2024-11-09 15:09

import django.core.validators
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
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('resource_type', models.CharField(choices=[('youtube', 'YouTube'), ('pdf', 'PDF'), ('other', 'Other')], max_length=10)),
                ('youtube_url', models.URLField(blank=True, null=True)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='resources/pdfs/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('other_file', models.FileField(blank=True, null=True, upload_to='resources/others/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_resources', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
