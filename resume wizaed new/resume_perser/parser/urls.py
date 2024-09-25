from django.urls import path
from .views import upload_resume, home

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_resume, name='upload_resume'),
]
