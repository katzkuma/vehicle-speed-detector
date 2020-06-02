from django.contrib import admin
from .models import Camera, TrafficRecord
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

# customize admin pages
class CameraAdmin(admin.ModelAdmin):
    # customize for add_form.html and change_form.html
    change_form_template = 'admin/website/website_change_form.html'
    list_display = ('camera_name', 'ip_address', 'camera_brand', 'enabled')
    actions = ['enable_camera_for_detection', 'disable_camera_for_detection']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset

    def enable_camera_for_detection(self, request, queryset):
        queryset.update(enabled=True)

    def disable_camera_for_detection(self, request, queryset):
        queryset.update(enabled=False)

    enable_camera_for_detection.short_description = "Enable selected camera for detection"
    disable_camera_for_detection.short_description = "Disable selected camera for detection"

class URLPathByBrandAdmin(admin.ModelAdmin):
    list_display = ('camera_brand', 'streamming_type', 'URLPath')