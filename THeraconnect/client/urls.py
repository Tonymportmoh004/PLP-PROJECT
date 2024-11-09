# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('appointments/create/', views.create_appointment, name='create_appointment'),
    path('appointments/<int:pk>/edit/', views.edit_appointment, name='edit_appointment'),
    path('appointments/<int:pk>/delete/', views.delete_appointment, name='delete_appointment'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('dashboard/', views.client_dashboard, name='client_dashboard'),
]
