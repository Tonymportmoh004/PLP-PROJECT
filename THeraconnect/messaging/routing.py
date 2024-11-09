from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/messages/<int:appointment_id>/', consumers.MessageConsumer.as_asgi()),
]
