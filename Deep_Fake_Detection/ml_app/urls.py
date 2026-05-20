"""project_settings URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import about, index, predict_page, cuda_full, image_upload, image_predict_page, landing_page

app_name = 'ml_app'
handler404 = views.handler404

urlpatterns = [
    path('', landing_page, name='landing'),  # Landing page as home
    path('video-detect/', index, name='home'),  # Video detection
    path('image-detect/', image_upload, name='image_upload'),  # Image detection
    path('about/', about, name='about'),
    path('predict/', predict_page, name='predict'),
    path('image-predict/', image_predict_page, name='image_predict'),
    path('cuda_full/', cuda_full, name='cuda_full'),
]