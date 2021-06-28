import requests
import cv2
import numpy as np

# Url to get the annotated image in image endpoint (local)
# url = "http://192.168.1.6:5000/image"
# Url to get the annotated image in image endpoint (production)
url = "http://34.136.195.110:5000/image"

# send HTTP request to the server
response = requests.get(url)

# Response for image endpoint
print('status_code: ', response.status_code)
annotated_image_bytes = response.content
# load the image and grab its spatial dimensions
annotated_image_array = np.fromstring(annotated_image_bytes, np.uint8)
# decode image
annotated_image = cv2.imdecode(annotated_image_array, cv2.IMREAD_COLOR)
print('Annotated image shape: ', annotated_image.shape)
# save the image
cv2.imwrite('hasil.jpg', annotated_image)
# show the image
cv2.imshow('Annotated image', annotated_image)
# waits for user to press any key 
# (this is necessary to avoid Python kernel form crashing)
cv2.waitKey(0) 
# closing all open windows 
cv2.destroyAllWindows() 