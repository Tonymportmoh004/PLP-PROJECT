# therapist/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TherapistSchedule
from .forms import TherapistScheduleForm as ScheduleForm, ConfirmAppointmentForm
from client.models import Appointment
from .forms import TherapistScheduleForm
@login_required
def create_schedule(request):
    # Check if the user has a profile and is a therapist
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'therapist':
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.therapist = request.user
            schedule.save()
            messages.success(request, "Schedule created successfully.")
            return redirect('schedule_list')
    else:
        form = ScheduleForm()

    return render(request, 'therapist/create_schedule.html', {'form': form})


# therapist/views.py
@login_required
def schedule_list(request):
    """View to list all schedules for the therapist."""
    schedules = TherapistSchedule.objects.filter(therapist=request.user).order_by('day_of_week', 'start_time')
    return render(request, 'therapist/schedule_list.html', {'schedules': schedules})

# therapist/views.py
@login_required
def edit_schedule(request, pk):
    """View for therapists to edit an existing schedule."""
    schedule = get_object_or_404(TherapistSchedule, pk=pk, therapist=request.user)
    form = TherapistScheduleForm(request.POST or None, instance=schedule)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Schedule updated successfully.")
        return redirect('schedule_list')
    
    return render(request, 'therapist/edit_schedule.html', {'form': form, 'schedule': schedule})

# therapist/views.py
from django.urls import reverse_lazy

@login_required
def delete_schedule(request, pk):
    """View for therapists to delete a schedule."""
    schedule = get_object_or_404(TherapistSchedule, pk=pk, therapist=request.user)
    
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, "Schedule deleted successfully.")
        return redirect('schedule_list')
    
    return render(request, 'therapist/delete_schedule.html', {'schedule': schedule})

# therapist/views.py
@login_required
def schedule_detail(request, pk):
    """View to display details of a specific schedule."""
    schedule = get_object_or_404(TherapistSchedule, pk=pk, therapist=request.user)
    return render(request, 'therapist/schedule_detail.html', {'schedule': schedule})



# therapist/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from client.models import Appointment
from messaging.models import Conversation

@login_required
def therapist_dashboard(request):
    if not request.user.is_therapist:
        return redirect('home')

    appointments = Appointment.objects.filter(therapist=request.user)
    conversations = Conversation.objects.filter(user1=request.user) | Conversation.objects.filter(user2=request.user)

    return render(request, 'therapist/dashboard.html', {'appointments': appointments, 'conversations': conversations})

@login_required
def update_appointment_status(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user != appointment.therapist:
        return redirect('therapist_dashboard')

    if request.method == 'POST':
        # Handle form submission to update status
        appointment.status = request.POST.get('status')
        appointment.zoom_link = request.POST.get('zoom_link')
        appointment.save()
        return redirect('therapist_dashboard')
    
    return render(request, 'therapist/update_appointment_status.html', {'appointment': appointment})


@login_required
def therapist_appointments(request):
    # Get all appointments for the logged-in therapist
    appointments = Appointment.objects.filter(therapist=request.user)
    
    return render(request, 'therapist/appointments_list.html', {'appointments': appointments})


