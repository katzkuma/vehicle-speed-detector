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

import cv2
from camera import loadCam
from camera import predict

import time
from matplotlib.patches import Rectangle

# for increasing webcam FPS with Python and OpenCV
#from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils

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
cameraAccount = 'root:0800'
cameraAdr = '169.254.18.191'
# video = cv2.VideoCapture(0)
#video = cv2.VideoCapture(rtspUrl)
# rtspUrl = 'rtsp://{}@{}/axis-media/media.amp?resolution=1280x720'.format(cameraAccount, cameraAdr)
rtspUrl = 0
vs = WebcamVideoStream(src=rtspUrl).start()
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
        predict.correct_yolo_boxes(boxes, image_h, image_w, input_h, input_w)

        
        

        # get the details of the detected objects
        v_boxes, v_labels, v_scores, v_boxid = predict.get_boxes(boxes, class_threshold)

        # summarize what we found
        for i in range(len(v_boxes)):
            print(v_labels[i], v_scores[i])
        # draw what we found
        predict.draw_boxes_cam(frame, v_boxes, v_labels, v_scores, v_boxid)

        #show the computed time
        elapsed_time = time.time() - starting_time
        fps=1/elapsed_time
        print("Time:"+str(round(elapsed_time,2))+" FPS:"+str(round(fps,2)))
        predict.draw_fps(frame, fps)

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

