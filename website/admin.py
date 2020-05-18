from django.contrib import admin
from .models import Camera, TrafficRecord
from django.contrib.auth.models import Group
from django.forms import ModelForm
from django import forms

# customize admin pages
class CameraAdmin(admin.ModelAdmin):
    # customize for add_form.html and change_form.html
    change_form_template = 'admin/website/website_change_form.html'

    # customize for add_form.html
    # add_form_template = 'admin/website/website_add_form.html'
    
    


# Register your models here.
admin.site.register(Camera, CameraAdmin)
admin.site.register(TrafficRecord)
admin.site.unregister(Group)

# change title on admin pages
admin.site.site_header = 'Administration for Traffic Situation System'

