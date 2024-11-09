import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from messaging import consumers
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # URL for the WebSocket connection
            path('ws/messages/<int:appointment_id>/', consumers.MessageConsumer.as_asgi()),
        ])
    ),
})
