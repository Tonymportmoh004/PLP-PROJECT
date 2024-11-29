from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('book', 'Book'),
        ('video', 'Video'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    file = models.FileField(upload_to='resources/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
