# import the necessary packages
from threading import Thread
import datetime
from cv2 import cv2
from imutils.video import WebcamVideoStream
from website.models import URLPathByBrand 

class VideoStream():
    def __init__(self, cameraSet=None):
        # initialize the dict for streamming objects
        self.cameras = dict()
        # initialize the dict for getting new frame
        self.frames = dict()
        # initialize the thread name
        self.name = 'Mutiple_Streammer_Thread'
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

        # initialize the video camera stream and read the first frame
        # from the stream
        if cameraSet is not None:
            for camera in cameraSet:
                url_path = URLPathByBrand.objects.get(camera_brand=camera.camera_brand, streamming_type=camera.streamming_type).URLPath
                
                # create streamming_url from data
                # the MAC is for the webcam of macbook 
                if camera.camera_brand == 'MAC':
                    streamming_url = 0
                else:
                    if camera.streamming_type == "IMAGE":
                        streamming_url = 'http://' + camera.camera_user + ':' + camera.camera_password + '@' + camera.ip_address + url_path
                    else:
                        streamming_url = 'rtsp://' + camera.camera_user + ':' + camera.camera_password + '@' + camera.ip_address + url_path
                self.cameras[camera.camera_name] = WebcamVideoStream(streamming_url, camera.camera_name).start()
    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            if self.stopped:
                for camera_name in self.cameras:
                    self.cameras[camera_name].stop()
                break
            else:
                for camera_name in self.cameras:
                    self.frames[camera_name] = self.cameras[camera_name].read()

    def read(self):
        return self.frames 

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True