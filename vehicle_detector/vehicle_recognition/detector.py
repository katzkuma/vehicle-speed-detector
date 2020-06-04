
import os
print('The backend of neural network is below:')
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import numpy as np
import json
from keras.models import load_model
from PIL import Image

from cv2 import cv2
from .camera import loadCam, predict
from .camera.videoStream import VideoStream
from .pusherService import pusherService

import time
from matplotlib.patches import Rectangle

# for increasing webcam FPS with Python and OpenCV
from imutils.video import FPS
from threading import Thread

from website.models import Camera, URLPathByBrand 

class Vehicle_Detector():
    def __init__(self):
        # initialize a variable for threading
        self.name = 'Detector_Thread'

        # initialize the variable used to indicate if the thread should be stopped
        self.stopped = True

        #Load the saved model
        self.model = load_model(os.path.join(BASE_DIR, 'parameter', 'yolov3.h5'))

        # initialize a variable for getting data form database
        self.cameraSet = None

        # initialize parameter of neural network
        self.font=cv2.FONT_HERSHEY_TRIPLEX
        self.points = []
        self.frame = []

        # initialize threads for getting img and run neural network
        self.vs = VideoStream(cameraSet=None)
        self.detector_thread = None

        # initialize the pusher service
        self.pusher = pusherService()
    
    def start(self):
        # turn detector on
        self.stopped = False

        # start to thread detector
        self.detector_thread = Thread(target=self.detect, name=self.name, args=())
        self.detector_thread.daemon = True
        self.detector_thread.start()
        return self

    def detect(self):
        # define the lastObjectDistance for calculating speed
        lastObjectDistance = 0

        # query all enables camera form database
        self.cameraSet = Camera.objects.all().filter(enabled = True)

        # initialize the thread for streamming video
        self.vs = VideoStream(self.cameraSet).start()
        print("[Detector] starting THREADED frames from web camera...")   
        
        # check if the thread should be stop
        if self.stopped is False:
            # start counting fps
            fpsCounter = FPS().start()

            while True:
                # check if the thread should be stop
                if self.stopped is True:
                    self.vs.stop()
                    break

                frames = self.vs.read()

                detected_result = {}
                
                # detect each camera
                for camera in self.cameraSet:
                    # get image from web camera
                    frame = frames[camera.camera_name]
                    if frame is None:
                        print('[Detector] Request img from camera time out: ' + camera.camera_name)
                    else:
                        # load and prepare image
                        image, image_w, image_h, input_w, input_h = loadCam.load_image_cam(frame)

                        # get region of interest by calling method
                        ROIframe = self.create_ROI_layer(frame.copy(), image_w, image_h, camera.region_of_interest)
                        
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
                        predict.correct_yolo_boxes(boxes, image_h, image_w, input_h, input_w, ROIframe)

                        # get the details of the detected objects
                        v_boxes, v_labels, v_scores, v_boxid = predict.get_boxes(boxes, class_threshold)

                        #show the computed time
                        elapsed_time = time.time() - starting_time
                        fps=1/elapsed_time
                        print("Time:"+str(round(elapsed_time,2))+" FPS:"+str(round(fps,2)))
                        predict.draw_fps(frame, fps)

                        print('Detected from ' + camera.camera_name + '(' + camera.ip_address + ')')
                        # summarize what we found
                        for i in range(len(v_boxes)):
                            print(v_labels[i], v_scores[i])
                        # draw what we found
                        newMovingSpeed, currentObjectDistance = predict.draw_boxes_cam(frame, v_boxes, v_labels, v_scores, v_boxid, elapsed_time, lastObjectDistance)

                        # creating the dict for storing detected result
                        detected_result[camera.camera_name] = [len(v_boxes), [float(camera.first_lat_recognition_section), float(camera.first_lon_recognition_section)], [float(camera.second_lat_recognition_section), float(camera.second_lon_recognition_section)]]

                        # saving current distance of detected object
                        lastObjectDistance = currentObjectDistance

                    # drawing detecting line on output form
                    # cv2.line(frame, self.points[0], self.points[1], (0, 0, 255), 5)
                    # cv2.line(frame, self.points[1], self.points[2], (0, 0, 255), 5)
                    # cv2.line(frame, self.points[2], self.points[3], (0, 0, 255), 5)
                    # cv2.line(frame, self.points[3], self.points[0], (0, 0, 255), 5)

                    # cv2.imshow("Capturing", frame)
                    fpsCounter.update()
                    key=cv2.waitKey(1)
                    if key == ord('q'):
                        break
                

                # # push detected result by using Pusher API
                # while True:
                #     if (datetime.datetime.now() - last_push_time).total_seconds() < 5:
                #         continue

                #     pusher = pusherService(detected_result)
                #     pusher.start()

                #     last_push_time = datetime.datetime.now()
                #     break
                
                self.pusher.push(detected_result)

                

            fpsCounter.stop()
            print("[INFO] elasped time: {:.2f}".format(fpsCounter.elapsed()))
            print("[INFO] approx. FPS: {:.2f}".format(fpsCounter.fps()))
        else:
            self.vs.stop()

    def stop(self):
        self.stopped = True
        print('[Detector] Detector has been shut down.')

    def create_ROI_layer(self, frame, width, height, ROIJson):
        # initialize a frame for creating a layer of region of interest
        ROIFrame = frame.copy()

        # get json of region of interest from data
        region_of_interest = json.loads(ROIJson)

        # initialize a array for adjusting points of region of interest
        points = []

        # make points is suitable for image from camera
        for key in region_of_interest:
            point = region_of_interest[key].split(',')
            points.append([(float(point[0]) * width), (float(point[1]) * height)])
        
        # make a array that the method fillPoly() need
        pointsForPoly = np.array(points,dtype=np.int32)

        # make a frame that region of interest need
        cv2.fillPoly(ROIFrame, [pointsForPoly], (0, 0, 255))

        return ROIFrame