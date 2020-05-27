from django.shortcuts import render, HttpResponse
from django.http import StreamingHttpResponse
from django.views import View
from .streamVideo.imgGenerate import generate

from website.models import URLPathByBrand



# Create your views here.

# traffic situation map
def index(request):
    return render(request, 'index.html')

# streaming video for admin page
def video_feed(request):
    resp = StreamingHttpResponse()

    ip_address = request.GET['ip_address']
    camera_user = request.GET['camera_user']
    camera_password = request.GET['camera_password']
    camera_brand = request.GET['camera_brand']
    streamming_type = request.GET['streamming_type']

    # URLPathByBranddata = URLPathByBrand()
    url_path = URLPathByBrand.objects.get(camera_brand=camera_brand, streamming_type=streamming_type).URLPath

    if streamming_type == "IMAGE":
        streamming_url = 'http://' + camera_user + ':' + camera_password + '@' + ip_address + url_path
    else:
        streamming_url = 'rtsp://' + camera_user + ':' + camera_password + '@' + ip_address + url_path

    try:
        generator = generate(streamming_url)
        if generator != 'error':
            resp = StreamingHttpResponse(generator, content_type="multipart/x-mixed-replace; boundary=frame")
            return resp
        else:
            print('video veeding is error of streaming.')
    except:
        resp.close()
        print('except on view.py')
        