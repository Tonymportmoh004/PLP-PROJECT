from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from datetime import timedelta, datetime, timezone
from django.apps import apps

User = get_user_model()

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
        
        Appointment = apps.get_model('clients', 'Appointment')
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


# therapist/models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_therapist = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Profile"
