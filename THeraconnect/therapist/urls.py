from django.urls import path
from . import views

app_name = 'therapist'

urlpatterns = [
    path('schedule/', views.schedule_list, name='schedule_list'),
    path('schedule/create/', views.create_schedule, name='create_schedule'),
    path('schedule/<int:pk>/', views.schedule_detail, name='schedule_detail'),
    path('schedule/<int:pk>/edit/', views.edit_schedule, name='edit_schedule'),
    path('schedule/<int:pk>/delete/', views.delete_schedule, name='delete_schedule'),
    path('dashboard/', views.therapist_dashboard, name='therapist_dashboard'),
    path('appointments/manage/', views.manage_appointments, name='manage_appointments'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:pk>/refer/', views.refer_appointment, name='refer_appointment'),
    
]
