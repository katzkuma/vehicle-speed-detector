from django.db import models
from django.forms import URLField as FormURLField
from django.core import validators

# the validators of URLFormField will not be changed automatically when the validators of URLField has been changed.

# create a RTSP version URLFormField
class RTSPURLFormField(FormURLField):
    default_validators = [validators.URLValidator(schemes=['rtsp'])]

# 
class RTSPURLField(models.URLField):  
    # URL field that accepts URLs that start with rtsp:// only
    default_validators = [validators.URLValidator(schemes=['rtsp'])]  

    # override formfield function for changing URLFormField
    def formfield(self, **kwargs):
        return super(RTSPURLField, self).formfield(**{
            'form_class': RTSPURLFormField,
        })