from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import HttpResponse
from .forms import UserRegistrationForm, ProfileForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib.auth.models import User
from .models import Profile
from .tokens import account_activation_token



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            send_verification_email(user, request)
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    return render(request, 'accounts/register.html', {'user_form': user_form, 'profile_form': profile_form})




def send_verification_email(user, request):
    mail_subject = 'Activate your account.'
    message = render_to_string('accounts/acc_active_email.html', {
        'user': user,
        'domain': request.get_host(),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    send_mail(mail_subject, message, 'your_email@example.com', [to_email])

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')


def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('home')

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'

@login_required
def delete_account(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('home')
    return render(request, 'accounts/delete_account.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile(request):
    user_profile = request.user.profile
    return render(request, 'accounts/profile.html', {'profile': user_profile})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit_profile.html', {'profile_form': profile_form})
