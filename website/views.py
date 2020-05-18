from django.shortcuts import render, HttpResponse
from django.http import StreamingHttpResponse
from django.views import View
from .streamVideo.imgGenerate import generate



# Create your views here.

# traffic situation map
def index(request):
    return render(request, 'index.html')

# streaming video for admin page
def video_feed(self, rtsp_url):
    resp = StreamingHttpResponse()
    try:
        generator = generate(rtsp_url)
        if generator != 'error':
            resp = StreamingHttpResponse(generator, content_type = "multipart/x-mixed-replace; boundary=frame")
            return resp
        else:
            print('video veeding is error of streaming.')
    except:
        resp.close()
        print('except on view.py')
    

        