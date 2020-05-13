from django.db import models


# Create your models here.
class Camera(models.Model):
    camera_name = models.CharField(default="untitled", max_length=50)
    stream_url = models.URLField(default="http://camera.address/")
    camera_latitude = models.DecimalField(default=0, decimal_places=6, max_digits=9)
    camera_longitude = models.DecimalField(default=0, decimal_places=6, max_digits=9)
    focal_length = models.FloatField(default=0)
    camera_height = models.FloatField(default=0)
    region_of_interest = models.TextField(default='{ "first_point":[0, 0], "second_point":[0, 0], "third_point":[0, 0], "fourth_point":[0, 0] }')
    first_lat_recognition_section = models.DecimalField(default=0, decimal_places=6, max_digits=9)
    first_lon_recognition_section = models.DecimalField(default=0, decimal_places=6, max_digits=9)
    second_lat_recognition_section = models.DecimalField(default=0, decimal_places=6, max_digits=9)
    second_lon_recognition_section = models.DecimalField(default=0, decimal_places=6, max_digits=9)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=False)
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
