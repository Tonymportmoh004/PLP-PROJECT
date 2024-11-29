from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from therapist.models import TherapistSchedule, Appointment, Message
from .forms import TherapistScheduleForm, AppointmentForm
from django.core.paginator import Paginator
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()

def is_therapist(user):
    return hasattr(user, 'profile') and user.profile.role == 'therapist'

@login_required
@user_passes_test(is_therapist, login_url='home')
def create_schedule(request):
    """Allow therapists to create their weekly availability schedule."""
    if request.method == 'POST':
        form = TherapistScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.therapist = request.user

            # Prevent duplicate schedules for the same day
            if TherapistSchedule.objects.filter(
                therapist=request.user,
                day_of_week=schedule.day_of_week,
            ).exists():
                messages.error(
                    request, "You already have a schedule for this day. Please edit it instead."
                )
                return redirect('schedule_list')

            schedule.save()
            messages.success(request, "Your schedule has been created successfully.")
            return redirect('schedule_list')
    else:
        form = TherapistScheduleForm()

    return render(request, 'scheduling/create_schedule.html', {'form': form})

@login_required
@user_passes_test(is_therapist, login_url='home')
def schedule_list(request):
    """List all schedules for the logged-in therapist."""
    schedules = TherapistSchedule.objects.filter(
        therapist=request.user
    ).order_by('day_of_week', 'start_time')

    # Paginate schedules
    paginator = Paginator(schedules, 5)  # Show 5 schedules per page
    page_number = request.GET.get('page')
    page_schedules = paginator.get_page(page_number)

    return render(request, 'scheduling/schedule_list.html', {'schedules': page_schedules})

@login_required
@user_passes_test(is_therapist, login_url='home')
def edit_schedule(request, pk):
    """Allow therapists to edit an existing schedule."""
    schedule = get_object_or_404(TherapistSchedule, pk=pk, therapist=request.user)
    form = TherapistScheduleForm(request.POST or None, instance=schedule)

    if request.method == 'POST' and form.is_valid():
        updated_schedule = form.save(commit=False)

        # Prevent overlaps with other schedules
        if TherapistSchedule.objects.filter(
            therapist=request.user,
            day_of_week=updated_schedule.day_of_week,
        ).exclude(pk=schedule.pk).exists():
            messages.error(request, "A schedule for this day already exists.")
            return redirect('schedule_list')

        updated_schedule.save()
        messages.success(request, "Your schedule has been updated successfully.")
        return redirect('schedule_list')

    return render(request, 'scheduling/edit_schedule.html', {'form': form, 'schedule': schedule})

@login_required
@user_passes_test(is_therapist, login_url='home')
def delete_schedule(request, pk):
    """Allow therapists to delete a specific schedule."""
    schedule = get_object_or_404(TherapistSchedule, pk=pk, therapist=request.user)

    if request.method == 'POST':
        schedule.delete()
        messages.success(request, "Your schedule has been deleted successfully.")
        return redirect('schedule_list')

    return render(request, 'scheduling/delete_schedule.html', {'schedule': schedule})

@login_required
@user_passes_test(is_therapist, login_url='home')
def schedule_detail(request, pk):
    """Display details of a specific schedule, including available slots."""
    schedule = get_object_or_404(TherapistSchedule, pk=pk, therapist=request.user)

    # Generate available slots for today or a chosen day
    selected_date = request.GET.get('date')
    date = datetime.strptime(selected_date, "%Y-%m-%d").date() if selected_date else now().date()
    available_slots = schedule.available_slots(date)

    return render(
        request, 
        'scheduling/schedule_detail.html', 
        {'schedule': schedule, 'available_slots': available_slots, 'date': date}
    )

@login_required
@user_passes_test(is_therapist, login_url='home')
def therapist_dashboard(request):
    """Dashboard view for therapists."""
    # Fetch upcoming appointments for the logged-in therapist
    appointments = Appointment.objects.filter(
        therapist=request.user,
        date__gte=now().date(),
    ).order_by('date', 'start_time')

    # Fetch all schedules for quick navigation
    schedules = TherapistSchedule.objects.filter(
        therapist=request.user
    ).order_by('day_of_week', 'start_time')

    # Generate a unique room name for the therapist
    room_name = f'therapist_{request.user.id}'

    return render(
        request,
        'scheduling/therapist_dashboard.html',
        {
            'appointments': appointments,
            'schedules': schedules,
            'room_name': room_name,  # Pass the room name to the template
        }
    )

@login_required
@user_passes_test(is_therapist, login_url='home')
def manage_appointments(request):
    """View to manage therapist's appointments."""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.therapist = request.user
            appointment.save()
            messages.success(request, "Appointment has been created successfully.")
            return redirect('therapist_dashboard')
    else:
        form = AppointmentForm()

    return render(request, 'scheduling/manage_appointments.html', {'form': form})

@login_required
@user_passes_test(is_therapist, login_url='home')
def appointment_detail(request, pk):
    """View details of a specific appointment."""
    appointment = get_object_or_404(Appointment, pk=pk, therapist=request.user)
    messages = Message.objects.filter(appointment=appointment).order_by('timestamp')

    return render(
        request,
        'scheduling/appointment_detail.html',
        {'appointment': appointment, 'messages': messages}
    )

@login_required
@user_passes_test(is_therapist, login_url='home')
def refer_appointment(request, pk):
    """Allow therapists to refer an appointment to another therapist."""
    appointment = get_object_or_404(Appointment, pk=pk, therapist=request.user)
    if request.method == 'POST':
        new_therapist_id = request.POST.get('new_therapist_id')
        new_therapist = get_object_or_404(User, pk=new_therapist_id, profile__role='therapist')
        appointment.therapist = new_therapist
        appointment.save()
        messages.success(request, "Appointment has been referred successfully.")
        return redirect('therapist_dashboard')

    therapists = User.objects.filter(profile__role='therapist').exclude(pk=request.user.pk)
    return render(request, 'scheduling/refer_appointment.html', {'appointment': appointment, 'therapists': therapists})
