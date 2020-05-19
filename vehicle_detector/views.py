from django.shortcuts import render
# from .vehicle_recognition import detector

# Create your views here.
# traffic situation map
def index(request):
    # detector.start()
    return render(request, 'index.html')