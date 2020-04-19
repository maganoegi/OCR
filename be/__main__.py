

from flask import Flask, request, Response
import cv2
import numpy as np
import jsonpickle
import os

from lib import *
from lib.ml import train_model, evaluate_image
from lib.preprocessing import *

app = Flask(__name__)

def check_filesystem() -> None:
    """ creates the filesystem needed for the BE to function """
    this_dir = os.path.dirname(__file__)
    digits_dir = os.path.join(this_dir, 'digits')

    if not os.path.exists('model'):
        os.makedirs('model')

    if not os.path.exists('digits'):
        os.makedirs('digits')
    
    for i in range(10):
        target_dir = os.path.join(digits_dir, str(i))
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

@app.route("/api/train/<label>", methods=['POST'])
def submit_2_dataset(label) -> Response:
    """ preprocesses the received image and classifies it """
    check_filesystem()

    data = np.fromstring(request.data, np.uint8)

    processed_image = preprocess(data)

    append_to_dataset(processed_image, label)

    response = jsonpickle.encode({'message': 'image received. size={}x{}, label={}'.format(processed_image.shape[1], processed_image.shape[0], label)})


    return Response(response=response, status=200, mimetype="application/json")


@app.route("/api/train/<batch>/<testP>/<epochs>/<l2>", methods=['POST'])
def train(batch, testP, epochs, l2) -> Response:
    """ starts the training procedure """
    check_filesystem()
    batch = int(batch)
    testP = float(testP)
    epochs = int(epochs)
    l2 = int(l2)
    
    result_dict = train_model(batch, testP, epochs, l2)

    response = jsonpickle.encode(result_dict)

    return Response(response=response, status=200, mimetype="application/json")



@app.route("/api/test", methods=['POST'])
def evaluate() -> Response:
    """ evaluate the image using the already saved model and labels """
    check_filesystem()

    data = np.fromstring(request.data, np.uint8)

    processed_image = preprocess(data)

    result = evaluate_image(processed_image)

    response = jsonpickle.encode(result)

    return Response(response=response, status=200, mimetype="application/json")



if __name__ == "__main__":
    check_filesystem()
    app.run(debug=False, threaded=False, port=5000)
    # app.run(debug=False, threaded=False, host="192.168.1.146", port=5000)

