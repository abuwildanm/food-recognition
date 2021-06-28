import gradio as gr
import requests
from cv2 import cv2
import numpy as np
import os

# Server url in production
server_url = "http://34.136.195.110:5000/"

def get_prediction(img):
    # Url to get prediction in predict endpoint
    endpoint = "predict"
    url = os.path.join(server_url, endpoint)
    headers = {"content-type": "image/jpg"}

    # encode image
    _, image_encoded = cv2.imencode(".jpg", img)
    image_bytes = image_encoded.tostring()

    # send HTTP request to the server
    response = requests.post(url, data=image_bytes, headers=headers)

    # Response for prediction endpoint
    predictions = response.json()
    return predictions

def get_image():
    # Url to get the annotated image in image endpoint
    endpoint = "image"
    url = os.path.join(server_url, endpoint)
    # send HTTP request to the server
    response = requests.get(url)
    # Response for image endpoint
    annotated_image_bytes = response.content
    # load the image and grab its spatial dimensions
    annotated_image_array = np.fromstring(annotated_image_bytes, np.uint8)
    # decode image
    annotated_image = cv2.imdecode(annotated_image_array, cv2.IMREAD_COLOR)
    annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
    return annotated_image

def predict(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    prediction = get_prediction(img)
    annotated_image = get_image()
    return annotated_image, prediction

if __name__ == '__main__':
    input_image = gr.inputs.Image(label="Input Image")
    output_image = gr.outputs.Image(label="Output Image")
    outputs_json = gr.outputs.JSON(label="Output Result")

    sample_images = [["./images/test1.jpg"], 
                     ["./images/test2.jpg"],
                     ["./images/test3.jpg"], 
                     ["./images/test4.jpg"]]
    app_description = "This web app is the web version of Dieter. \
                    In this web application you will know how \
                    the Indonesian Food Recognition feature of \
                    Dieter works. You simply upload a picture of \
                    Indonesian food and our model will recognize \
                    the food and give you the result. We will only \
                    activate this web application until July 5, 2021"
    
    iface = gr.Interface(predict, 
                        inputs=input_image, 
                        outputs=[output_image, outputs_json], 
                        title="Dieter Food Recognition", 
                        server_name="0.0.0.0", 
                        server_port=8080,
                        allow_screenshot=True, 
                        allow_flagging=False,
                        description=app_description,
                        examples=sample_images)
    iface.launch()