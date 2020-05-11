from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon

# Create your models here.
class CameraList(models.Model):
    camera_name = models.CharField(default="untitled", max_length=50)
    stream_url = models.TextField(default="unsetted")
    camera_latitude = models.DecimalField
    camera_longitude = models.DecimalField
    focal_length = models.FloatField
    camera_height = models.FloatField
    region_of_interest = models.PolygonField(default=Polygon(((0, 0), (0, 0), (0, 0), (0, 0), (0, 0))))
    recognition_section = models.LineStringField
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=False)
    class Meta:
        db_table = "camera_list"

class TrafficHistory(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    recognition_section = models.LineStringField
    detected_vehicles = models.IntegerField
    time_mean_speed = models.FloatField
    class Meta:
        db_table = "traffic_history"
