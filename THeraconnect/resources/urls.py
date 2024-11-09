from django.urls import path
from . import views

urlpatterns = [
    path('resource/<int:pk>/', views.resource_detail, name='resource_detail'),
    path('', views.resource_list, name='resource_list'),
    path('resource/create/', views.resource_create, name='create_resource'),
    path('resource/edit/<int:pk>/', views.resource_edit, name='edit_resource'),
    path('resource/delete/<int:pk>/', views.resource_delete, name='delete_resource'),
]
