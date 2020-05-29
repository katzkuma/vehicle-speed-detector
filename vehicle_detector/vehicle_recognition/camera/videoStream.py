# import the necessary packages
from threading import Thread
import datetime
from cv2 import cv2

class VideoStream():
	def __init__(self, src=None, name="WebcamVideoStream"):
		# initialize the video camera stream and read the first frame
		# from the stream
		if src != None:
			self.stream = cv2.VideoCapture(src)
			(self.grabbed, self.frame) = self.stream.read()

		# initialize the thread name
		self.name = name

		# initialize url of streamming
		self.url = src

		# initialize a frame
		self.frame = None

		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = True

	def start(self):
		self.stopped = False
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, name=self.name, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				self.stream = cv2.VideoCapture(None)
				return
			
			if self.url is not None:
				self.stream = cv2.VideoCapture(self.url)
				# otherwise, read the next frame from the stream
				(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		start_time = datetime.datetime.now()
		while (datetime.datetime.now() - start_time).total_seconds() < 6 :
			if self.frame is not None:
				newFrame = self.frame
				self.frame =  None
				# return the frame most recently read
				return newFrame
		return None 
		

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True

	def source(self, url):
		self.url = url

	# def isURLNone(self):
	# 	return True if self.url is None else False