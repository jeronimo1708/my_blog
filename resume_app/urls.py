# blog_project/resume_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'), # Defines the root URL for this app
]