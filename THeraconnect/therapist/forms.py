from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from .models import TherapistSchedule, Appointment, Message
from django.forms.widgets import TimeInput


class TherapistScheduleForm(forms.ModelForm):
    class Meta:
        model = TherapistSchedule
        fields = ['day_of_week', 'start_time', 'end_time', 'break_start', 'break_end']
        widgets = {
            'start_time': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'break_start': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'break_end': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('day_of_week', css_class='form-group col-md-4 mb-0'),
                Column('start_time', css_class='form-group col-md-4 mb-0'),
                Column('end_time', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('break_start', css_class='form-group col-md-6 mb-0'),
                Column('break_end', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Save Schedule')
        )

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        break_start = cleaned_data.get('break_start')
        break_end = cleaned_data.get('break_end')
        
        if start_time and end_time and start_time >= end_time:
            self.add_error('end_time', "End time must be after start time.")
        
        if break_start and break_end:
            if not (start_time < break_start < break_end < end_time):
                self.add_error('break_end', "Break times must be within start and end times.")
        elif break_start or break_end:
            self.add_error('break_start', "Both break start and end times must be provided.")
        
        return cleaned_data

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['client', 'date', 'start_time', 'end_time', 'zoom_link', 'status', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
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
                Column('client', css_class='form-group col-md-6 mb-0'),
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
            Submit('submit', 'Save Appointment')
        )
