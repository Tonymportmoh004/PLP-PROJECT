from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Resource(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ('youtube', 'YouTube'),
        ('pdf', 'PDF'),
        ('other', 'Other'),
    ]

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_resources')
    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPE_CHOICES)
    youtube_url = models.URLField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='resources/pdfs/', validators=[FileExtensionValidator(['pdf'])], blank=True, null=True)
    other_file = models.FileField(upload_to='resources/others/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
