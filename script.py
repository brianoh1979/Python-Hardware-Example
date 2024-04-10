# import the necessary packages
# library for https requests
import requests
# library for operating system dependent functionality such as read or write a file
import os,time
# Picamera Library is Raspberry Pi specfic and allows control of camera modules
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
# initialize the Keras REST API endpoint URL along with the input
# image path
# initialize camera
camera = PiCamera()
camera.vflip=True
rawCapture = PiRGBArray(camera)

# Keras is Deep Learning module for Python. Here we are taking Keras model and deploying as a REST API (platform app). 
KERAS_REST_API_URL = "https://objectdetection407.herokuapp.com/predict"
IMAGE_PATH = "image.jpg"

#Sleep for 5 seconds
time.sleep(5)

#input variables used within camera.capture method (function which belongs to object - PiCamera / camera in this case) for image and video.
camera.capture(rawCapture, format="bgr")
image = rawCapture.array
print(image)
# display the image on screen and wait for a keypress
camera.stop_preview()
camera.close()
cv2.imwrite("image.jpg", image)
cv2.waitKey(0)
# load the input image and construct the payload for the request
image = open(IMAGE_PATH, "rb").read()

payload = {"image": image}

# submit the request and have the Keras Model analyze it via REST API call
r = requests.post(KERAS_REST_API_URL, files=payload).json()

# ensure the request was successful
if r["success"]:
    # loop over the predictions and display them
    for (i, result) in enumerate(r["predictions"]):
        print(result["label"],result["x"],result["y"])
        os.system("espeak ' " + result["label"]+result["y"]+result["x"]+" '")
# otherwise, the request failed
else:
    print("Request failed")
