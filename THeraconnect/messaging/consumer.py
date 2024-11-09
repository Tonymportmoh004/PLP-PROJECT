import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Appointment, Message

User = get_user_model()

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.appointment_id = self.scope['url_route']['kwargs']['appointment_id']
        self.appointment_group_name = f"appointment_{self.appointment_id}"
        
        # Join the group
        await self.channel_layer.group_add(
            self.appointment_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.appointment_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        
        # Get the appointment
        appointment = Appointment.objects.get(id=self.appointment_id)
        
        # Get sender and receiver based on the appointment
        sender = self.scope['user']
        receiver = appointment.client if sender == appointment.therapist else appointment.therapist
        
        # Create a new message
        new_message = Message.objects.create(
            appointment=appointment,
            sender=sender,
            receiver=receiver,
            message=message
        )
        
        # Send the message to the group
        await self.channel_layer.group_send(
            self.appointment_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': timestamp
        }))
