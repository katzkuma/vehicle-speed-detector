## Traffic Situation System
---

with YOLOv3, LeafletJS, Django framework

### Run the following using:
1. Prepare and run Redis server from Docker
```
$ docker pull redis
$ docker run -d -p 6379:6379 --name redis redis
```

2. Run Django server
```
$ python manage.py runserver
```

#### References:
1. [WebSocket chatRoom with Django-Channels（一）](https://medium.com/@Sean_Hsu/websocket-chatroom-with-django-channels-f6c7bed7d2f4)
2. [How to Perform Object Detection With YOLOv3 in Keras](https://machinelearningmastery.com/how-to-perform-object-detection-with-yolov3-in-keras/)
3. [初探物件追蹤 Multiple Object Tracking(MOT)](https://medium.com/@peaceful0907/%E5%88%9D%E6%8E%A2%E7%89%A9%E4%BB%B6%E8%BF%BD%E8%B9%A4-multiple-object-tracking-mot-4f1b42e959f9)