# blog_project/resume_app/views.py
from django.shortcuts import render
from .data import RESUME_DATA # Import your resume data

def home_view(request):
    context = {
        'resume': RESUME_DATA # Pass the data to the template context
    }
    return render(request, 'resume_app/index.html', context)