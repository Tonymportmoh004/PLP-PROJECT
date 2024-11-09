# therapist/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('schedule/', views.schedule_list, name='schedule_list'),
    path('schedule/create/', views.create_schedule, name='create_schedule'),
    path('schedule/<int:pk>/', views.schedule_detail, name='schedule_detail'),
    path('schedule/<int:pk>/edit/', views.edit_schedule, name='edit_schedule'),
    path('schedule/<int:pk>/delete/', views.delete_schedule, name='delete_schedule'),
    
    
    path('dashboard/', views.therapist_dashboard, name='therapist_dashboard'),
    path('update_appointment_status/<int:appointment_id>/', views.update_appointment_status, name='update_appointment_status'),
]
