
from django.urls import path
from . import views

urlpatterns = [
    path('operator', views.operator),
]