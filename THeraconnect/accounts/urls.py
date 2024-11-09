from django.urls import path
from .views import register, profile, edit_profile, custom_login, custom_logout, activate, CustomPasswordResetView, CustomPasswordResetConfirmView, CustomPasswordResetDoneView, CustomPasswordResetCompleteView, delete_account

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('delete_account/', delete_account, name='delete_account'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]
