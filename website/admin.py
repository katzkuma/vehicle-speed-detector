from django.contrib import admin
from .models import Camera, TrafficRecord
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

# customize admin pages
class CameraAdmin(admin.ModelAdmin):
    # customize for add_form.html and change_form.html
    change_form_template = 'admin/website/website_change_form.html'

    def get_queryset(self, request):
        print(CameraAdmin)
        print(self)
        queryset = super().get_queryset(request)
        print(queryset)
        return queryset

    # customize for add_form.html
    # add_form_template = 'admin/website/website_add_form.html'



