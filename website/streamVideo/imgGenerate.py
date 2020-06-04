from imutils.video import VideoStream
from cv2 import cv2

def generate(rtsp_url):
    	# create a variable  to store output frame
    outputFrame = None

    # request video streaming from inputted URL
    vs = VideoStream(src=rtsp_url).start()

    
    try:
        # loop over frames from the output stream
        while True:
            outputFrame = vs.read()
            if outputFrame is None:
                break

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

            # yield the output frame in the byte format
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
        
        vs.stop()
    except:
        vs.stop()
        return 'error'
            