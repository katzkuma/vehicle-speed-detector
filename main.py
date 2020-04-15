#!/usr/bin/env python
# coding: utf-8
# based on https://github.com/experiencor/keras-yolo3

import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

import numpy as np
from keras.layers import Input
from keras.layers.merge import add
from keras.models import Model, load_model
from PIL import Image

from cv2 import cv2
from camera import loadCam
from camera import predict
from webApp import web

import time
from matplotlib.patches import Rectangle

# for increasing webcam FPS with Python and OpenCV
#from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils

web.start()

#Load the saved model
model = load_model('yolov3.h5')

#using imutils, construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] starting THREADED frames from webcam...")

# camera for testing
axisCameraAccount = 'root:0800'
axisCameraAdr = '169.254.18.191'

# lounge room camera
loungeCameraAccount = 'root:pass'
loungeCameraAdr = '10.220.200.238'

# old function for getting vedio stream
# video = cv2.VideoCapture(0)
# video = cv2.VideoCapture(rtspUrl)

# camera url
webCamUrl = 0
axisUrl = 'rtsp://{}@{}/axis-media/media.amp?resolution=1280x720'.format(axisCameraAccount, axisCameraAdr)
loungeUrl = 'rtsp://{}@{}/axis-media/media.amp?resolution=1280x720'.format(loungeCameraAccount, loungeCameraAdr)

# streamming video by subthread
vs = WebcamVideoStream(src=axisUrl).start()

# define the lastObjectDistance for calculating speed
lastObjectDistance = 0

font=cv2.FONT_HERSHEY_TRIPLEX
points = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)
        points.append((x, y))



frame = vs.read()

# creating a hotspot layout
hotspot = frame.copy()
cv2.imshow("Capturing", frame)
cv2.setMouseCallback('Capturing', click_event)

while True:
    frame = vs.read()

    # guiding of setting hotspot area
    if len(points) == 4:
        # showing guiding text
        cv2.putText(frame,'Do you want to start detecting with these hotspot? (y/n)',(40,40),font,1,(38, 15, 245),2)

        # removing event of mouse click
        cv2.setMouseCallback('Capturing', lambda *args : None)

        # drawing detecting line on hotspot layout
        hotspot = frame.copy()
        cv2.line(hotspot, points[0], points[1], (0, 0, 255), 150)
        cv2.line(hotspot, points[2], points[3], (0, 0, 255), 150)
        
        # hotspot area is unfinished
        # cv2.rectangle(frame, points[0], points[1], (0, 0, 255), -1)
        # cv2.rectangle(frame, points[2], points[3], (0, 0, 255), -1)

        # drawing detecting line on output form
        cv2.line(frame, points[0], points[1], (0, 0, 255), 5)
        cv2.line(frame, points[2], points[3], (0, 0, 255), 5)

        # checking hotspot area (press Y to continue, N to restart setting)
        keyYN=cv2.waitKey(1)
        if keyYN == ord('y'):
            break
        elif keyYN == ord('n'):
            cv2.setMouseCallback('Capturing', click_event)
            points = []
            pass
        pass
    elif len(points) >= 2:
        # showing guiding text
        cv2.putText(frame,'Choose a hotspot on second of the road.',(40,40),font,1,(38, 15, 245),2)

        # preview the hotspot line
        cv2.line(frame, points[0], points[1], (0, 0, 255), 5)
        if len(points) == 3:
            cv2.circle(frame, points[2], 3, (38, 15, 245), -1)
        pass
    elif len(points) < 2:
        # showing guiding text
        cv2.putText(frame,'Choose a hotspot on first of the road.',(40,40),font,1,(38, 15, 245),2)

        # preview the hotspot line
        if len(points) == 1:
            cv2.circle(frame, points[0], 3, (38, 15, 245), -1)
        pass
    else :
        pass

    cv2.imshow("Capturing", frame)

    # press Q to quit the application
    key2=cv2.waitKey(1)
    if key2 == ord('q'):
        # reset a list of hotspot setting
        points = []
        break

# checking for the setting of hotspot
if len(points) == 4:
    fpsCounter = FPS().start()
    while True:
        #_, frame = video.read()
        frame = vs.read()

        # load and prepare image
        image, image_w, image_h, input_w, input_h = loadCam.load_image_cam(frame)
        
        # make prediction and start to time
        starting_time= time.time()
        yhat = model.predict(image)
        # summarize the shape of the list of arrays
        print([a.shape for a in yhat])
        # define the anchors
        anchors = [[116,90, 156,198, 373,326], [30,61, 62,45, 59,119], [10,13, 16,30, 33,23]]
        # define the probability threshold for detected objects
        class_threshold = 0.6
        boxes = list()
        for i in range(len(yhat)):
            # decode the output of the network
            boxes += predict.decode_netout(yhat[i][0], anchors[i], class_threshold, input_h, input_w)
        # suppress non-maximal boxes
        predict.do_nms(boxes, 0.5)
        # correct the sizes of the bounding boxes for the shape of the image
        predict.correct_yolo_boxes(boxes, image_h, image_w, input_h, input_w, hotspot)

        
        

        # get the details of the detected objects
        v_boxes, v_labels, v_scores, v_boxid = predict.get_boxes(boxes, class_threshold)

        #show the computed time
        elapsed_time = time.time() - starting_time
        fps=1/elapsed_time
        print("Time:"+str(round(elapsed_time,2))+" FPS:"+str(round(fps,2)))
        predict.draw_fps(frame, fps)

        # summarize what we found
        for i in range(len(v_boxes)):
            print(v_labels[i], v_scores[i])
        # draw what we found
        newMovingDistance, currentObjectDistance = predict.draw_boxes_cam(frame, v_boxes, v_labels, v_scores, v_boxid, elapsed_time, lastObjectDistance)
        # saving current distance of detected object
        lastObjectDistance = currentObjectDistance

        # drawing detecting line on output form
        cv2.line(frame, points[0], points[1], (0, 0, 255), 5)
        cv2.line(frame, points[2], points[3], (0, 0, 255), 5)

        cv2.imshow("Capturing", frame)
        fpsCounter.update()
        key=cv2.waitKey(1)
        if key == ord('q'):
                break
                    

    fpsCounter.stop()
    print("[INFO] elasped time: {:.2f}".format(fpsCounter.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fpsCounter.fps()))

vs.stop()
cv2.destroyAllWindows()

