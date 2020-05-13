from django.contrib import admin
from .models import Camera, TrafficRecord

# Register your models here.
admin.site.register(Camera)
admin.site.register(TrafficRecord)