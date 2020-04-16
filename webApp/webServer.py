#coding=UTF-8
import os	#Python的標準庫中的os模組包含普遍的作業系統功能
import re	#引入正則表示式物件
import urllib	#用於對URL進行編解碼
from http.server import HTTPServer, BaseHTTPRequestHandler  #匯入HTTP處理相關的模組
import http.server
import socketserver
from threading import Thread
import json

data = {'result': 'this is a test'}


class webServer:
	def __init__(self, name="webServer"):
		self.name = name
		self.PORT = 8080
		self.Handler = http.server.SimpleHTTPRequestHandler
		self.server = socketserver.TCPServer(("", self.PORT), self.Handler)
		self.server.allow_reuse_address = True

	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.start_server, name=self.name, args=())
		t.daemon = True
		t.start()
		return self

	#啟動服務函式
	def start_server(self):
		print("serving at port", self.PORT)
		self.server.serve_forever()

	# 停止服務函式 
	def close_server(self):
		print("closing at port", self.PORT)
		self.server.shutdown()
		



