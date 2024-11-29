from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from therapist.models import Appointment, TherapistSchedule
from messaging.models import Message
from .models import Feedback
from .forms import FeedbackForm, AppointmentForm
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()

def is_client(user):
    return hasattr(user, 'profile') and user.profile.role == 'client'

@login_required
@user_passes_test(is_client, login_url='home')
def client_dashboard(request):
    """Dashboard view for clients."""
    # Fetch upcoming appointments for the logged-in client
    appointments = Appointment.objects.filter(
        client=request.user,
        date__gte=now().date(),
    ).order_by('date', 'start_time')

    # Fetch all schedules for the client's therapist
    therapist_schedules = TherapistSchedule.objects.filter(
        therapist__in=[appointment.therapist for appointment in appointments]
    ).order_by('day_of_week', 'start_time')

    return render(
        request,
        'clients/dashboard.html',
        {
            'appointments': appointments,
            'therapist_schedules': therapist_schedules,
        }
    )

@login_required
@user_passes_test(is_client, login_url='home')
def appointment_detail(request, pk):
    """View details of a specific appointment."""
    appointment = get_object_or_404(Appointment, pk=pk, client=request.user)
    messages = Message.objects.filter(appointment=appointment).order_by('timestamp')
    feedback = Feedback.objects.filter(appointment=appointment).first()

    return render(
        request,
        'clients/appointment_detail.html',
        {'appointment': appointment, 'messages': messages, 'feedback': feedback}
    )

@login_required
@user_passes_test(is_client, login_url='home')
def give_feedback(request, pk):
    """Allow clients to give feedback for a specific appointment."""
    appointment = get_object_or_404(Appointment, pk=pk, client=request.user)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.appointment = appointment
            feedback.client = request.user
            feedback.therapist = appointment.therapist
            feedback.save()
            return redirect('client_dashboard')
    else:
        form = FeedbackForm()

    return render(request, 'clients/give_feedback.html', {'form': form, 'appointment': appointment})

@login_required
@user_passes_test(is_client, login_url='home')
def book_appointment(request):
    """Allow clients to book an appointment with their therapist."""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.save()
            return redirect('client_dashboard')
    else:
        form = AppointmentForm()

    return render(request, 'clients/book_appointment.html', {'form': form})

@login_required
@user_passes_test(is_client, login_url='home')
def view_appointments(request):
    """View all appointments for the logged-in client."""
    appointments = Appointment.objects.filter(client=request.user).order_by('date', 'start_time')
    return render(request, 'clients/view_appointments.html', {'appointments': appointments})

@login_required
@user_passes_test(is_client, login_url='home')
def find_therapist(request):
    """Allow clients to find a therapist."""
    therapists = User.objects.filter(profile__role='therapist')
    query = request.GET.get('q')
    if query:
        therapists = therapists.filter(username__icontains=query)
    return render(request, 'clients/find_therapist.html', {'therapists': therapists, 'query': query})
