from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta, timezone
from django.apps import apps
from django.core.exceptions import ValidationError

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_therapist = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Profile"

class TherapistSchedule(models.Model):
    therapist = models.ForeignKey(User, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=[(i, day) for i, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])])
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_start = models.TimeField(null=True, blank=True)
    break_end = models.TimeField(null=True, blank=True)

    def is_within_schedule(self, start_time, end_time):
        """Check if given time range is within schedule, considering breaks."""
        within_hours = self.start_time <= start_time and end_time <= self.end_time
        if self.break_start and self.break_end:
            outside_break = (end_time <= self.break_start or start_time >= self.break_end)
            return within_hours and outside_break
        return within_hours

    def available_slots(self, date=None):
        """Generate available 30-minute slots within the schedule, excluding break times and existing appointments."""
        date = date or timezone.now().date()
        slots = []
        slot_start = datetime.combine(date, self.start_time)
        end_datetime = datetime.combine(date, self.end_time)
        
        Appointment = apps.get_model('therapist', 'Appointment')
        while slot_start + timedelta(minutes=30) <= end_datetime:
            slot_end = slot_start + timedelta(minutes=30)
            # Skip slots during break times
            if self.break_start and self.break_end:
                break_start_datetime = datetime.combine(date, self.break_start)
                break_end_datetime = datetime.combine(date, self.break_end)
                if slot_start >= break_start_datetime and slot_end <= break_end_datetime:
                    slot_start = slot_end
                    continue
            
            # Check if slot overlaps with any existing appointment
            if not Appointment.objects.filter(
                therapist=self.therapist,
                date=date,
                start_time__lt=slot_end.time(),
                end_time__gt=slot_start.time()
            ).exists():
                slots.append({'start_time': slot_start.time(), 'end_time': slot_end.time()})
            
            slot_start = slot_end

        return slots

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
    notes = models.TextField(blank=True, null=True)

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

class Message(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='therapist_sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"
