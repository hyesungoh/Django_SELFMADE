from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class diary_home(TemplateView):
    template_name = "diary_home.html"