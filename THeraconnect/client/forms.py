from django import forms
from .models import Appointment
from therapist.models import TherapistSchedule
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['therapist', 'date', 'start_time', 'end_time', 'status']

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
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
                Column('status', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Book Appointment')
        )

        # Apply date restriction (cannot choose past dates)
        self.fields['date'].widget.attrs.update({'min': timezone.now().date().isoformat()})
        
        # Add time picker classes
        self.fields['start_time'].widget.attrs.update({'class': 'timepicker'})
        self.fields['end_time'].widget.attrs.update({'class': 'timepicker'})

        # Dynamically populate available times for start_time and end_time
        if 'therapist' in self.data:
            therapist_id = self.data.get('therapist')
            if therapist_id:
                available_times = TherapistSchedule.objects.filter(therapist_id=therapist_id)
                start_choices = [(ts.start_time.strftime('%H:%M'), ts.start_time.strftime('%H:%M')) for ts in available_times]
                end_choices = [(ts.end_time.strftime('%H:%M'), ts.end_time.strftime('%H:%M')) for ts in available_times]
                self.fields['start_time'].choices = start_choices
                self.fields['end_time'].choices = end_choices
