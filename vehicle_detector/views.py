from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .vehicle_recognition.detector import Vehicle_Detector

vehicle_detector = Vehicle_Detector()

# Create your views here.
# traffic situation map
def operator(request):
    operation = request.POST['switchArg']

    if operation == 'ON':
        vehicle_detector.start()
    else:
        vehicle_detector.stop()
    
    return HttpResponseRedirect("/admin/")
        
    
     