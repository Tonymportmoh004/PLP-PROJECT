from django.urls import path
from . import views

urlpatterns = [
    path('chat/<int:appointment_id>/', views.chat_view, name='chat_view'),
]
