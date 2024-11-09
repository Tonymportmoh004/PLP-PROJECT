from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Appointment
from .forms import AppointmentForm
from therapist.models import TherapistSchedule
from django.core.paginator import Paginator
from django.contrib.auth.models import User

def check_date_and_schedule(therapist, date, start_time, end_time):
    """Helper to ensure the date is valid and within the therapist's schedule."""
    if date < timezone.now().date():
        return "The selected date cannot be in the past."

    weekday = date.weekday()
    therapist_schedule = TherapistSchedule.objects.filter(
        therapist=therapist, day_of_week=weekday
    ).first()
    if not therapist_schedule or not therapist_schedule.is_within_schedule(start_time, end_time):
        return "The selected time is outside the therapist's available hours."

    return None  # Indicates no errors

def check_conflict(therapist, date, start_time, end_time, exclude_pk=None):
    """Helper to check for conflicting appointments."""
    conflicts = Appointment.objects.filter(
        therapist=therapist,
        date=date,
        start_time__lt=end_time,
        end_time__gt=start_time
    )
    if exclude_pk:
        conflicts = conflicts.exclude(pk=exclude_pk)
    return conflicts.exists()

@login_required
def create_appointment(request):
    """View for creating a new appointment with real-time conflict and schedule checks."""
    form = AppointmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.instance.client = request.user
        therapist = form.cleaned_data['therapist']
        date = form.cleaned_data['date']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        
        date_schedule_error = check_date_and_schedule(therapist, date, start_time, end_time)
        if date_schedule_error:
            messages.error(request, date_schedule_error)
        elif check_conflict(therapist, date, start_time, end_time):
            messages.error(request, "This time slot is already booked. Please choose another.")
        else:
            form.save()
            messages.success(request, "Appointment created successfully.")
            return redirect(reverse('appointment_list'))
    
    return render(request, 'clients/book_appointments.html', {'form': form})

@login_required
def edit_appointment(request, pk):
    """View for editing an existing appointment with conflict and schedule checks."""
    appointment = get_object_or_404(Appointment, pk=pk)
    form = AppointmentForm(request.POST or None, instance=appointment)
    
    if request.method == 'POST' and form.is_valid():
        form.instance.client = request.user
        therapist = form.cleaned_data['therapist']
        date = form.cleaned_data['date']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']

        date_schedule_error = check_date_and_schedule(therapist, date, start_time, end_time)
        if date_schedule_error:
            messages.error(request, date_schedule_error)
        elif check_conflict(therapist, date, start_time, end_time, exclude_pk=appointment.pk):
            messages.error(request, "This time slot is already booked. Please choose another.")
        else:
            form.save()
            messages.success(request, "Appointment updated successfully.")
            return redirect(reverse('appointment_list'))
    
    return render(request, 'clients/edit_appointment.html', {'form': form, 'appointment': appointment})

@login_required
def delete_appointment(request, pk):
    """View to delete an appointment."""
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, "Appointment deleted successfully.")
        return redirect(reverse('appointment_list'))
    return render(request, 'clients/delete_appointment.html', {'appointment': appointment})

@login_required
def appointment_list(request):
    """View to list all appointments in a paginated format."""
    appointments = Appointment.objects.select_related('therapist', 'client').all()
    paginator = Paginator(appointments, 10)  # Show 10 appointments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'clients/appointment_list.html', {'page_obj': page_obj})

@login_required
def appointment_detail(request, pk):
    """View to display detailed information about a specific appointment."""
    appointment = get_object_or_404(Appointment.objects.select_related('therapist', 'client'), pk=pk)
    return render(request, 'clients/appointment_detail.html', {'appointment': appointment})

@login_required
def check_availability(request):
    """AJAX view to check available slots for a given therapist and date."""
    therapist_id = request.GET.get('therapist_id')
    date = request.GET.get('date')
    slots = []

    if therapist_id and date:
        therapist = get_object_or_404(User, id=therapist_id)
        date = timezone.datetime.strptime(date, '%Y-%m-%d').date()
        
        weekday = date.weekday()
        therapist_schedule = TherapistSchedule.objects.filter(therapist=therapist, day_of_week=weekday).first()
        if therapist_schedule:
            slots = therapist_schedule.available_slots()

    return JsonResponse({'slots': slots})


# client/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment
from messaging.models import Conversation

@login_required
def client_dashboard(request):
    if not request.user.is_client:
        return redirect('home')

    appointments = Appointment.objects.filter(client=request.user)
    conversations = Conversation.objects.filter(user1=request.user) | Conversation.objects.filter(user2=request.user)

    return render(request, 'client/dashboard.html', {'appointments': appointments, 'conversations': conversations})
