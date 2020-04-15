#coding=UTF-8
import os	#Python的標準庫中的os模組包含普遍的作業系統功能
import re	#引入正則表示式物件
import urllib	#用於對URL進行編解碼
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler  #匯入HTTP處理相關的模組
from threading import Thread

def start(self):
    # start the thread to read frames from the video stream
    t = Thread(target=self.start_server, name=self.name, args=())
    t.daemon = True
    t.start()
    return self

#自定義處理程式，用於處理HTTP請求
class TestHTTPHandler(BaseHTTPRequestHandler):
	#處理GET請求
	def do_GET(self):
		#頁面輸出模板字串
		templateStr = '''  
			<html>  
				<head>  
					<title>QR Link Generator</title>  
				</head>  
				<body>
				%s
				<br>  
				<br>  
					<form action="/qr" name=f method="GET">
						<input maxLength=1024 size=70 name=s value="" title="Text to QR Encode">
						<input type=submit value="Show QR" name=qr>  
					</form>
				</body>  
			</html> '''


		# 將正則表示式編譯成Pattern物件,其中r是raw的意思，表示對字串不進行轉義  print("\bhi")-->hi print(r"\bhi")-->\bhi
		pattern = re.compile(r'/qr\?s=([^\&]+)\&qr=Show\+QR')
		# 使用Pattern匹配文字，獲得匹配結果，無法匹配時將返回None
		match = pattern.match(self.path)
		print(self.path)
		qrImg = ''
			
		if match:
			# 使用Match獲得分組資訊,match.group(1)是url後面的引數，match.group(0)是url本身。。。
			qrImg = '<img src="http://chart.apis.google.com/chart?chs=300x300&cht=qr&choe=UTF-8&chl=' + match.group(1) + '" /><br />' + urllib.unquote(match.group(1)) 
			print(qrImg)

		self.protocal_version = 'HTTP/1.1'	#設定協議版本
		self.send_response(200)	#設定響應狀態碼
		self.send_header("Contect", "Welcome")	#設定響應頭
		self.end_headers()
		self.wfile.write(templateStr % qrImg)	#輸出響應內容
	
#啟動服務函式
def start_server(port):
    http_server = HTTPServer(('', int(port)), TestHTTPHandler)
    http_server.serve_forever()	#設定一直監聽並接收請求

#os.chdir('d:')	#改變工作目錄到 static 目錄
start_server(8080)	#啟動服務，監聽8080埠
