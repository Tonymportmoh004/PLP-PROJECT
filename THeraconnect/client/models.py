from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta, datetime
from django.apps import apps

User = get_user_model()

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    therapist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='therapist_appointments')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    zoom_link = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ['client', 'therapist', 'date', 'start_time', 'end_time']
        ordering = ['date', 'start_time']
        indexes = [
            models.Index(fields=['therapist', 'date', 'start_time', 'end_time']),
        ]

    def clean(self):
        # Ensure date is not in the past
        if self.date and self.date < timezone.now().date():
            raise ValidationError("The appointment date cannot be in the past.")
        
        # Check if start_time and end_time are provided
        if not self.start_time or not self.end_time:
            raise ValidationError("Both start and end times are required for the appointment.")

        # Ensure that start_time is before end_time
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")
        
        # Ensure appointment falls within therapist's available schedule
        if not self.is_within_therapist_schedule():
            raise ValidationError("This time slot is not available with the therapist.")
        
        # Check for overlapping appointments
        overlapping_appointments = Appointment.objects.filter(
            therapist=self.therapist,
            date=self.date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk)
        
        if overlapping_appointments.exists():
            raise ValidationError("This time slot is already booked.")

    def is_within_therapist_schedule(self):
        """Check if the appointment falls within the therapist's schedule for the day."""
        TherapistSchedule = apps.get_model('therapist', 'TherapistSchedule')
        weekday = self.date.weekday()
        schedule = TherapistSchedule.objects.filter(therapist=self.therapist, day_of_week=weekday).first()
        return schedule.is_within_schedule(self.start_time, self.end_time) if schedule else False
