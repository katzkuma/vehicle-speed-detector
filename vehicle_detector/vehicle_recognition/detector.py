import os
print('The backend of neural network is below:')
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import numpy as np
from keras.layers import Input
from keras.layers.merge import add
from keras.models import Model, load_model
from PIL import Image

from cv2 import cv2
from .camera import loadCam
from .camera import predict
from .pusherService import pusherService

import time
from matplotlib.patches import Rectangle

# for increasing webcam FPS with Python and OpenCV
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils

from threading import Thread

class Vehicle_Detector():
    def __init__(self):
        # initialize a variable for threading
        self.name = 'Detector_Thread'
        # initialize the variable used to indicate if the thread should be stopped
        self.stopped = True
        #Load the saved model
        self.model = load_model(os.path.join(BASE_DIR, 'parameter', 'yolov3.h5'))

        # # camera for testing
        # axisCameraAccount = 'root:0800'
        # axisCameraAdr = '169.254.18.191'

        # # lounge room camera
        # loungeCameraAccount = 'root:pass'
        # loungeCameraAdr = '10.220.200.238'

        # camera url
        self.webCamUrl = 0
        # axisUrl = 'rtsp://{}@{}/axis-media/media.amp?resolution=1280x720'.format(axisCameraAccount, axisCameraAdr)
        # loungeUrl = 'rtsp://{}@{}/axis-media/media.amp?resolution=1280x720'.format(loungeCameraAccount, loungeCameraAdr)

        self.font=cv2.FONT_HERSHEY_TRIPLEX
        self.points = []
        self.frame = []
        self.vs = WebcamVideoStream(src=None)
        self.thread = Thread()
    
    def start(self):
        self.stopped = False
        self.thread = Thread(target=self.detect, name=self.name, args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    def detect(self):
        # define the lastObjectDistance for calculating speed
        lastObjectDistance = 0
        # streamming video by subthread
        self.vs = WebcamVideoStream(src=self.webCamUrl).start()
        print("[INFO] starting THREADED frames from webcam...")
        # initialize a array for storing points
        self.points = []
        # initialize a layout for setting region of interest
        self.ROIframe = self.vs.read()        

        while True:
            if self.stopped is True:
                self.vs.stop()
                break

            frame = self.vs.read()

            # guiding of setting hotspot area
            if len(self.points) == 4:
                # showing guiding text
                cv2.putText(frame,'Do you want to start detecting with these hotspot? (y/n)',(40,40),self.font,1,(38, 15, 245),2)

                # removing event of mouse click
                cv2.setMouseCallback('Capturing', lambda *args : None)

                # drawing detecting area on ROI layout
                pointsForPoly = np.array(self.points,dtype=np.int32)
                cv2.fillPoly(self.ROIframe, [pointsForPoly], (0, 0, 255))

                # drawing detecting line on output form
                cv2.line(frame, self.points[0], self.points[1], (0, 0, 255), 5)
                cv2.line(frame, self.points[1], self.points[2], (0, 0, 255), 5)
                cv2.line(frame, self.points[2], self.points[3], (0, 0, 255), 5)
                cv2.line(frame, self.points[3], self.points[0], (0, 0, 255), 5)

                # checking hotspot area (press Y to continue, N to restart setting)
                keyYN=cv2.waitKey(1)
                if keyYN == ord('y'):
                    break
                elif keyYN == ord('n'):
                    # cv2.setMouseCallback('Capturing', click_event)
                    self.points = []
                    pass
                pass
            elif len(self.points) >= 2:
                # showing guiding text
                cv2.putText(frame,'Choose 4 point for a hotspot.',(40,40),self.font,1,(38, 15, 245),2)

                # preview the hotspot line
                cv2.line(frame, self.points[0], self.points[1], (0, 0, 255), 5)
                if len(self.points) == 3:
                    cv2.circle(frame, self.points[2], 3, (38, 15, 245), -1)
                pass
            elif len(self.points) < 2:
                # showing guiding text
                cv2.putText(frame,'Choose 4 point for a hotspot.',(40,40),self.font,1,(38, 15, 245),2)

                # preview the hotspot line
                if len(self.points) == 1:
                    cv2.circle(frame, self.points[0], 3, (38, 15, 245), -1)
                pass
            else :
                pass

            # cv2.imshow("Capturing", frame)

            # press Q to quit the application
            key2=cv2.waitKey(1)
            if key2 == ord('q'):
                    # reset a list of hotspot setting
                    self.points = []
                    break

        
        if self.stopped is False:
            # checking for the setting of hotspot
            if len(self.points) == 4:
                fpsCounter = FPS().start()
                while True:
                    if self.stopped is True:
                        self.vs.stop()
                        break

                    #_, frame = video.read()
                    frame = self.vs.read()

                    # load and prepare image
                    image, image_w, image_h, input_w, input_h = loadCam.load_image_cam(frame)
                    
                    # make prediction and start to time
                    starting_time= time.time()
                    yhat = self.model.predict(image)
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
                    predict.correct_yolo_boxes(boxes, image_h, image_w, input_h, input_w, self.ROIframe)

                    
                    

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
                    newMovingSpeed, currentObjectDistance = predict.draw_boxes_cam(frame, v_boxes, v_labels, v_scores, v_boxid, elapsed_time, lastObjectDistance)

                    pusher = pusherService(newMovingSpeed)
                    pusher.start()

                    # saving current distance of detected object
                    lastObjectDistance = currentObjectDistance

                    # drawing detecting line on output form
                    cv2.line(frame, self.points[0], self.points[1], (0, 0, 255), 5)
                    cv2.line(frame, self.points[1], self.points[2], (0, 0, 255), 5)
                    cv2.line(frame, self.points[2], self.points[3], (0, 0, 255), 5)
                    cv2.line(frame, self.points[3], self.points[0], (0, 0, 255), 5)

                    # cv2.imshow("Capturing", frame)
                    fpsCounter.update()
                    key=cv2.waitKey(1)
                    if key == ord('q'):
                        break

            fpsCounter.stop()
            print("[INFO] elasped time: {:.2f}".format(fpsCounter.elapsed()))
            print("[INFO] approx. FPS: {:.2f}".format(fpsCounter.fps()))

            print('start detecting')
        else:
            self.vs.stop()
    def stop(self):
        self.stopped = True
        print('Detector has been shut down.')