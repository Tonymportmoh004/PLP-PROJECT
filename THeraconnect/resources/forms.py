from django import forms
from .models import Resource

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'resource_type', 'youtube_url', 'pdf_file', 'other_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['youtube_url'].widget.attrs.update({'class': 'form-control'})
        self.fields['pdf_file'].widget.attrs.update({'class': 'form-control'})
        self.fields['other_file'].widget.attrs.update({'class': 'form-control'})
