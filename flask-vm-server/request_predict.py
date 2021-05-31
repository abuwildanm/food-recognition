import requests
import cv2
import numpy as np

# Url to get prediction in predict endpoint (local)
# url = "http://192.168.1.6:5000/predict"
# Url to get prediction in predict endpoint (production)
url = "http://34.136.195.110:5000/predict"
headers = {"content-type": "image/jpg"}

# encode image
image = cv2.imread('images/test1.jpg')
_, image_encoded = cv2.imencode(".jpg", image)
image_bytes = image_encoded.tostring()

# send HTTP request to the server
response = requests.post(url, data=image_bytes, headers=headers)

# Response for prediction endpoint
predictions = response.json()
print('status_code: ', response.status_code)
print('predictions: ', predictions)