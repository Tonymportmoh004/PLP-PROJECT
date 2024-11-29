from django.shortcuts import render, get_object_or_404
from therapist.models import Appointment
from .models import Conversation, Message

def chat_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    conversation, created = Conversation.objects.get_or_create(appointment=appointment)
    messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
    room_name = appointment_id

    return render(request, 'messaging/chat.html', {
        'appointment': appointment,
        'messages': messages,
        'room_name': room_name,
    })
