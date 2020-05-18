
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('video_feed/<path:rtsp_url>', views.video_feed)    # for streaming video on admin pages
]