from django.urls import path
from . import views
from .views import home
urlpatterns = [
    path('', home, name='home'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-and-conditions/', views.TermsAndConditionsView.as_view(), name='terms_conditions'),
]
