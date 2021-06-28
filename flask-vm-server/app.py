import os
import numpy as np
import cv2
from flask import Flask, jsonify, request, Response, abort, send_file
from yolo import get_predictions

app = Flask(__name__)

@app.route("/")
def index():
    return "Selamat datang di indomaret, selamat berbelanja"

@app.route("/predict", methods=["POST"])
def predict():
    # load input image and grab its spatial dimensions
    image_array = np.fromstring(request.data, np.uint8)
    # decode image
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # prediction process
    predictions = get_predictions(request)

    # annotate the image
    for pred in predictions:
        # print prediction
        # print(pred)

        # extract the bounding box coordinates
        (x, y) = (pred["boxes"][0], pred["boxes"][1])
        (w, h) = (pred["boxes"][2], pred["boxes"][3])

        # draw a bounding box rectangle and label on the image
        cv2.rectangle(image, (x, y), (x + w, y + h), pred["color"], 2)
        text = "{}: {:.4f}".format(pred["label"], pred["confidence"])
        cv2.putText(
            image, 
            text, 
            (x, y - 5), 
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5, 
            pred["color"], 
            2
        )

    # save annotated image
    cv2.imwrite("annotated_image.jpg", image)

    return jsonify(predictions)

@app.route("/image", methods=["GET"])
def get_annotated_image():
    try:
        # Cara 1
        # prepare image for response
        # image = cv2.imread('annotated_image.jpg')
        # _, img_encoded = cv2.imencode(".jpg", image)
        # image_bytes = img_encoded.tostring()
        # return Response(response=image_bytes, status=200, mimetype='image/jpeg')

        # Cara 2
        return send_file('annotated_image.jpg')
    except FileNotFoundError:
        abort(404, 'File not found! Please make a prediction first')

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5000, debug=False)
    app.run(host="0.0.0.0", port=5000, debug=True) # comment this code if deploy on production