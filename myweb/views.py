from django.shortcuts import render
from django.views import generic

def aboutViews(request):
    template_name = 'about.html'
    return render(request, template_name)