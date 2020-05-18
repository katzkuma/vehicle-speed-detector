from django.db import models
from .adminModels import cameraModels



# Create your models here.
class Camera(models.Model):
    enabled = models.BooleanField(default=False)
    camera_name = models.CharField(default="untitled", max_length=50)
    stream_url = cameraModels.RTSPURLField(default="rtsp://camera.address/")
    camera_user = models.CharField(default="", max_length=50)
    camera_password = models.CharField(default="", max_length=50)

    CAMERA_BRAND_CHOICES = [
        ('AXIS', 'Axis'),
        ('GEO', 'GeoVision'),
        ('VIVO', 'VIVOTEK'),
    ]
    camera_brand = models.CharField(
        max_length=5,
        choices=CAMERA_BRAND_CHOICES,
        default='GEO',
    )

    STREAM_RESOLUTION_CHOICES = [
        ('4K', '4096x2160'),
        ('2K', '2560x1440'),
        ('1080P', '1920x1080'),
        ('720P', '1280x720'),
    ]
    stream_resolution = models.CharField(
        max_length=5,
        choices=STREAM_RESOLUTION_CHOICES,
        default='1080P',
    )

    region_of_interest = models.TextField(default='{ "first_point":[0, 0], "second_point":[0, 0], "third_point":[0, 0], "fourth_point":[0, 0] }')

    camera_latitude = models.DecimalField(default=0, decimal_places=6, max_digits=9)
    camera_longitude = models.DecimalField(default=0, decimal_places=6, max_digits=9)
    focal_length = models.FloatField(default=0)
    camera_height = models.FloatField(default=0)
    first_lat_recognition_section = models.DecimalField(default=0, decimal_places=6, max_digits=9)
    first_lon_recognition_section = models.DecimalField(default=0, decimal_places=6, max_digits=9)
    second_lat_recognition_section = models.DecimalField(default=0, decimal_places=6, max_digits=9)
    second_lon_recognition_section = models.DecimalField(default=0, decimal_places=6, max_digits=9)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "tsd_camera_list"

class TrafficRecord(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_lat_recognition_section = models.DecimalField(default=0, decimal_places=6, max_digits=9)
    first_lon_recognition_section = models.DecimalField(default=0, decimal_places=6, max_digits=9)
    second_lat_recognition_section = models.DecimalField(default=0, decimal_places=6, max_digits=9)
    second_lon_recognition_section = models.DecimalField(default=0, decimal_places=6, max_digits=9)
    detected_vehicles = models.IntegerField(default=0)
    time_mean_speed = models.FloatField(default=0)
    class Meta:
        db_table = "tsd_traffic_history"


