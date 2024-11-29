from django import forms
from therapist.models import Appointment
from .models import Feedback
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.utils import timezone
from therapist.models import TherapistSchedule

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comments']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('rating', css_class='form-group col-md-6 mb-0'),
                Column('comments', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Submit Feedback')
        )

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['therapist', 'date', 'start_time', 'end_time', 'zoom_link', 'status', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'zoom_link': forms.URLInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('therapist', css_class='form-group col-md-6 mb-0'),
                Column('date', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('start_time', css_class='form-group col-md-6 mb-0'),
                Column('end_time', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('zoom_link', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('status', css_class='form-group col-md-6 mb-0'),
                Column('notes', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Book Appointment')
        )

        # Apply restriction: Date cannot be in the past
        self.fields['date'].widget.attrs.update({'min': timezone.now().date().isoformat()})

    def clean(self):
        """Custom validation for date and time conflicts."""
        cleaned_data = super().clean()
        therapist = cleaned_data.get('therapist')
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if therapist and date:
            weekday = date.weekday()

            # Validate that the selected times fall within the therapist's schedule
            therapist_schedule = TherapistSchedule.objects.filter(
                therapist=therapist, day_of_week=weekday
            ).first()

            if not therapist_schedule:
                raise forms.ValidationError("The selected therapist is not available on this date.")
            if not therapist_schedule.is_within_schedule(start_time, end_time):
                raise forms.ValidationError("The selected time is outside the therapist's available hours.")

        # Ensure start time is before end time
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("Start time must be earlier than end time.")

        return cleaned_data
