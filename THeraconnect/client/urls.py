from django.urls import path
from . import views

app_name = 'client'

urlpatterns = [
    path('dashboard/', views.client_dashboard, name='client_dashboard'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:pk>/feedback/', views.give_feedback, name='give_feedback'),
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('appointments/', views.view_appointments, name='view_appointments'),
    path('find_therapist/', views.find_therapist, name='find_therapist'),
    
]
