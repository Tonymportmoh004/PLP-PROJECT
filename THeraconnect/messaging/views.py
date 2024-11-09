# messaging/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from client.models import Appointment

@login_required
def conversation_view(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    if request.user not in [conversation.user1, conversation.user2]:
        return redirect('dashboard')

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            Message.objects.create(conversation=conversation, sender=request.user, content=message)
            return redirect('conversation', conversation_id=conversation.id)
    
    messages = conversation.messages.all().order_by('timestamp')

    return render(request, 'messaging/conversation_view.html', {'conversation': conversation, 'messages': messages})
