# blog_app/urls.py
from django.urls import path
from . import views

app_name = 'blog_app' # <--- THIS IS THE NAMESPACE WE USED IN blog_project/urls.py

urlpatterns = [
    # post list
    path('', views.post_list, name='post_list'),
    # post detail
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/like/', views.post_like, name='post_like'),
]