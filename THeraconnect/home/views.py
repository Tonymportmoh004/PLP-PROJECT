from django.shortcuts import render

def home(request):
    return render(request, 'home/index.html')
from django.views.generic import TemplateView

class PrivacyPolicyView(TemplateView):
    template_name = 'privacy_policy.html'

class TermsAndConditionsView(TemplateView):
    template_name = 'terms_and_conditions.html'
