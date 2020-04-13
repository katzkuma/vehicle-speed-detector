from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from numpy import expand_dims
import cv2

# load and prepare an image
def load_image_pixels(filename, shape):
    # load the image to get its shape
    image = load_img(filename)
    width, height = image.size
    # load the image with the required size
    image = load_img(filename, target_size=shape)
    # convert to numpy array
    image = img_to_array(image)
    # scale pixel values to [0, 1]
    image = image.astype('float32')
    image /= 255.0
    # add a dimension so that we have one sqqample
    image = expand_dims(image, 0)
    return image, width, height

# load and prepare an image from cam
def load_image_cam(frame):
    # load the frame to get its shape
    image = frame
    height,width,channels = image.shape
    # resizeRate = 0.2
    # input_h, input_w = int(height * resizeRate), int(width * resizeRate)
    input_h, input_w = 416, 416
    shape = (input_w, input_h)
    

    image = cv2.resize(image, shape) 

    # change dtype to float32
    image = image.astype('float32')
    # scale pixel values to [0, 1]
    image /= 255.0
    # add a dimension so that we have one sample
    image = expand_dims(image, 0)
    return image, width, height, input_w, input_h