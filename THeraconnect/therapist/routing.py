from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/therapist/(?P<room_name>\w+)/$', consumers.TherapistConsumer.as_asgi()),
]
