import os
import numpy as np
import math
from cv2 import cv2 

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# define the labels
labels = []
with open(os.path.join(BASE_DIR, 'parameter', "coco.names"), "r") as f:
    labels = [line.strip() for line in f.readlines()]
font = cv2.FONT_HERSHEY_PLAIN
colors= np.random.uniform(0,255,size=(len(labels),3))

def decode_netout(netout, anchors, obj_thresh, net_h, net_w):
    grid_h, grid_w = netout.shape[:2]
    nb_box = 3
    netout = netout.reshape((grid_h, grid_w, nb_box, -1))
    # nb_class = netout.shape[-1] - 5
    boxes = []
    netout[..., :2]  = _sigmoid(netout[..., :2])
    netout[..., 4:]  = _sigmoid(netout[..., 4:])
    netout[..., 5:]  = netout[..., 4][..., np.newaxis] * netout[..., 5:]
    netout[..., 5:] *= netout[..., 5:] > obj_thresh
 
    for i in range(grid_h*grid_w):
        row = i / grid_w
        col = i % grid_w
        for b in range(nb_box):
            # 4th element is objectness score
            objectness = netout[int(row)][int(col)][b][4]
            if(objectness.all() <= obj_thresh): continue
            # exclude the objects which is not human, car, bus or truck
            if(netout[int(row)][col][b][5:][0] == 0 and netout[int(row)][col][b][5:][2] == 0 and netout[int(row)][col][b][5:][5] == 0 and netout[int(row)][col][b][5:][7] == 0): continue
            # first 4 elements are x, y, w, and h
            x, y, w, h = netout[int(row)][int(col)][b][:4]
            x = (col + x) / grid_w # center position, unit: image width
            y = (row + y) / grid_h # center position, unit: image height
            w = anchors[2 * b + 0] * np.exp(w) / net_w # unit: image width
            h = anchors[2 * b + 1] * np.exp(h) / net_h # unit: image height
            # last elements are class probabilities
            classes = netout[int(row)][col][b][5:]
            box = BoundBox(x-w/2, y-h/2, x+w/2, y+h/2, objectness, classes)
            boxes.append(box)
    return boxes

def _sigmoid(x):
    return 1. / (1. + np.exp(-x))

class BoundBox:
    def __init__(self, xmin, ymin, xmax, ymax, objness = None, classes = None):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.objness = objness
        self.classes = classes
        self.label = -1
        self.score = -1
 
    def get_label(self):
        if self.label == -1:
            self.label = np.argmax(self.classes)
 
        return self.label
 
    def get_score(self):
        if self.score == -1:
            self.score = self.classes[self.get_label()]
 
        return self.score

def correct_yolo_boxes(boxes, image_h, image_w, net_h, net_w):
    new_w, new_h = net_w, net_h
    for i in range(len(boxes)):
        x_offset, x_scale = (net_w - new_w)/2./net_w, float(new_w)/net_w
        y_offset, y_scale = (net_h - new_h)/2./net_h, float(new_h)/net_h
        boxes[i].xmin = int((boxes[i].xmin - x_offset) / x_scale * image_w)
        boxes[i].xmax = int((boxes[i].xmax - x_offset) / x_scale * image_w)
        boxes[i].ymin = int((boxes[i].ymin - y_offset) / y_scale * image_h)
        boxes[i].ymax = int((boxes[i].ymax - y_offset) / y_scale * image_h)


def do_nms(boxes, nms_thresh):
    if len(boxes) > 0:
        nb_class = len(boxes[0].classes)
    else:
        return
    for c in range(nb_class):
        sorted_indices = np.argsort([-box.classes[c] for box in boxes])
        for i in range(len(sorted_indices)):
            index_i = sorted_indices[i]
            if boxes[index_i].classes[c] == 0: continue
            for j in range(i+1, len(sorted_indices)):
                index_j = sorted_indices[j]
                if bbox_iou(boxes[index_i], boxes[index_j]) >= nms_thresh:
                    boxes[index_j].classes[c] = 0
def bbox_iou(box1, box2):
    intersect_w = _interval_overlap([box1.xmin, box1.xmax], [box2.xmin, box2.xmax])
    intersect_h = _interval_overlap([box1.ymin, box1.ymax], [box2.ymin, box2.ymax])
    intersect = intersect_w * intersect_h
    w1, h1 = box1.xmax-box1.xmin, box1.ymax-box1.ymin
    w2, h2 = box2.xmax-box2.xmin, box2.ymax-box2.ymin
    union = w1*h1 + w2*h2 - intersect
    return float(intersect) / union


def _interval_overlap(interval_a, interval_b):
    x1, x2 = interval_a
    x3, x4 = interval_b
    if x3 < x1:
        if x4 < x1:
            return 0
        else:
            return min(x2, x4) - x1
    else:
        if x2 < x3:
             return 0
        else:
            return min(x2, x4) - x3
        
# get all of the results above a threshold
def get_boxes(input_boxes, thresh, ROI_frame):
    # initialize a dict to seperate
    boxes = {
                'person': {'boxes': [], 'labels': [], 'scores': [], 'cx': [], 'cy': []}, 
                'vehicle': {'boxes': [], 'labels': [], 'scores': [], 'cx': [], 'cy': []}
            }
    # enumerate all boxes
    for input_box in input_boxes:
        # enumerate all possible labels
        for i in range(len(labels)):
            # check if the threshold for this label is high enough
            if input_box.classes[i] > thresh:
                # seperate boxes to person and vehicle
                if input_box.get_label() == 0:
                    boxes['person']['boxes'].append(input_box)
                    boxes['person']['labels'].append(input_box.get_label())
                    boxes['person']['scores'].append(input_box.classes[i]*100)
                    boxes['person']['cx'].append((input_box.xmin + input_box.xmax) / 2)
                    boxes['person']['cy'].append((input_box.ymin + input_box.ymax) / 2)
                else:
                    cx = (input_box.xmin + input_box.xmax) / 2
                    cy = (input_box.ymin + input_box.ymax) / 2
                    if (ROI_filter(cx, cy, ROI_frame) is False): continue
                    boxes['vehicle']['boxes'].append(input_box)
                    boxes['vehicle']['labels'].append(input_box.get_label())
                    boxes['vehicle']['scores'].append(input_box.classes[i]*100)
                    boxes['vehicle']['cx'].append(cx)
                    boxes['vehicle']['cy'].append(cy)
                # don't break, many labels may trigger for one box
    return boxes

def ROI_filter(cx, cy, roi):
    if cx > 80 and cx < 1200 and cy > 60 and cy < 700:
        if (roi[int(cy), int(cx)] == [0, 0, 255]).all():
            return True
    return False

# draw all results
def draw_boxes_cam(frame, v_boxes, v_labels, v_scores, v_boxid, elapsed_time, lastObjectDistance):
    # draw each box
    for i in range(len(v_boxes)):
        box = v_boxes[i]
        # get coordinates
        y1, x1, y2, x2 = box.ymin, box.xmin, box.ymax, box.xmax
        width, height = x2 - x1, y2 - y1

        # get label and confidence of detected object for showing it in top left corner
        label = v_labels[i]
        confidence= v_scores[i]
        
        # call calculating function
        newMovingDistance, currentObjectDistance = calculateMovingDistance(width, lastObjectDistance)
        
        # calculate velocity and convert unit from m/s to km/h
        movingSpeed = newMovingDistance / elapsed_time * 1000 / 3600

        # showing speed, text and score in top left corner
        # cv2.putText(frame,label+" "+str(round(confidence, 2)) + " speed:" + str(round(movingSpeed, 2)) + "(km/h)",(x1,y1+30),font,3,(255,0,0),4)
        cv2.putText(frame,"speed:" + str(round(movingSpeed, 2)) + "(km/h)",(x1,y1+30),font,3,(255,0,0),4)

        # draw the box
        color = colors[v_boxid[i]]
        cv2.rectangle(frame,(x1,y1),(x1+width,y1+height),color,2)

        return str(round(movingSpeed, 2)), currentObjectDistance
    return 0, 0


def calculateMovingDistance(widthPixels, lastObjectDistance):
    # focal length of camera (mm)
    focalLength = 5.5
    # real width of detected object (cm)
    objectWidth = 55
    # real distance between center of person and camera in lounge room (m)
    loungeCameraHeight = 1.54
    # real height of camera for testing (m)
    testingCameraHeight = 0
    # define a moving distance for calculating
    movingDistance = 0

    # getting the distance between object and camera ,formula: L = F * WC / px
    currentObjectDistance = focalLength * objectWidth / widthPixels

    
    if lastObjectDistance == 0:
        return 0, currentObjectDistance
    elif lastObjectDistance > 0:
        # calculating moving distance
        currentDistance = np.square(currentObjectDistance) - np.square(testingCameraHeight)
        lastDistance = np.square(lastObjectDistance) - np.square(testingCameraHeight)

        # make sure the math domin over zero before square rooting 
        if currentDistance > 0 and lastDistance > 0:
            movingDistance = math.sqrt(currentDistance) - math.sqrt(lastDistance)
            pass

        return movingDistance, currentObjectDistance
    else:
        print('calculating error in calculateSpeed func.')
        pass


# draw FPS
def draw_fps(frame, fps):
    cv2.putText(frame,"FPS:"+str(round(fps,2)),(10,50),font,2,(10,10,10),1)