# the routing.py is used to correspond url path and consumers
# It's for channels package
from django.urls import re_path
from website import consumers

websocket_urlpatterns = [
  re_path(r'^ws/push/', consumers.ChatConsumer),
]