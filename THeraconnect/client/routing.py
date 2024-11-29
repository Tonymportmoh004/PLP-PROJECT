from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/client/(?P<room_name>\w+)/$', consumers.ClientConsumer.as_asgi()),
]
