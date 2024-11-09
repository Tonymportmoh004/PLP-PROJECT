from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

class UserRegistrationForm(UserCreationForm):
    
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', css_class='form-control'),
            Field('email', css_class='form-control'),
            Field('password1', css_class='form-control'),
            Field('password2', css_class='form-control')
        )
        self.helper.add_input(Submit('submit', 'Register'))



class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', css_class='form-control'),
            Field('password', css_class='form-control')
        )
        self.helper.add_input(Submit('submit', 'Login'))

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('email', css_class='form-control')
        )
        self.helper.add_input(Submit('submit', 'Reset Password'))

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('new_password1', css_class='form-control'),
            Field('new_password2', css_class='form-control')
        )
        self.helper.add_input(Submit('submit', 'Set Password'))


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES, 
        required=True, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'role']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('first_name', css_class='form-control'),
            Field('last_name', css_class='form-control'),
            Field('phone_number', css_class='form-control'),
            Field('address', css_class='form-control'),
            Field('role', css_class='form-control')
        )
        self.helper.add_input(Submit('submit', 'Save'))
