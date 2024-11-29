from django.db import models
from django.contrib.auth import get_user_model
from therapist.models import Appointment

User = get_user_model()

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    therapist = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clients')

    def __str__(self):
        return f"{self.user.username} Profile"

class Feedback(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='feedback')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    therapist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_feedbacks')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Feedback by {self.client} for {self.therapist} on {self.appointment.date}"
