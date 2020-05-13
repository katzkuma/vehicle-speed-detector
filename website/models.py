from django.db import models


# Create your models here.
class Camera(models.Model):
    camera_name = models.CharField(default="untitled", max_length=50)
    stream_url = models.TextField(default="unsetted")
    camera_latitude = models.DecimalField
    camera_longitude = models.DecimalField
    focal_length = models.FloatField
    camera_height = models.FloatField
    region_of_interest = models.TextField(default="((0, 0), (0, 0), (0, 0), (0, 0))")
    first_lat_recognition_section = models.DecimalField
    first_lon_recognition_section = models.DecimalField
    second_lat_recognition_section = models.DecimalField
    second_lon_recognition_section = models.DecimalField
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=False)
    class Meta:
        db_table = "tsd_camera_list"

class TrafficRecord(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_lat_recognition_section = models.DecimalField
    first_lon_recognition_section = models.DecimalField
    second_lat_recognition_section = models.DecimalField
    second_lon_recognition_section = models.DecimalField
    detected_vehicles = models.IntegerField
    time_mean_speed = models.FloatField
    class Meta:
        db_table = "tsd_traffic_history"
