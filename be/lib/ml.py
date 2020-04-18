


import matplotlib
matplotlib.use("Agg")

from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from keras.models import Sequential, load_model
from keras.layers.core import Dense
from keras.optimizers import SGD
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import pickle
import cv2
import os

this_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(this_dir)
dataset_path = os.path.join(base_path, "digits")
model_path = os.path.join(base_path, "model", "digit_nn.model")
label_path = os.path.join(base_path, "model", "digit_nn_lb.pickle")
plot_path = os.path.join(base_path, "model", "digit_nn_plot.png")
test_path = os.path.join(base_path, "test_images")

def train_model(batch, testP, epochs, l2) -> dict:
    """ trains the model based on saved images and FE variables """
        
    data = []
    labels = []
    # shuffle the image paths
    imagePaths = sorted(list(paths.list_images(dataset_path)))
    random.seed(42)
    random.shuffle(imagePaths)
    for imagePath in imagePaths:
        # flatten the image, and organize the data and labels
        image = cv2.imread(imagePath).flatten()
        data.append(image)
        label = imagePath.split(os.path.sep)[-2]
        labels.append(label)

    # map the pixel value space to [0, 1] space
    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)

    # split the dataset into training and testing parts by %
    (trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=testP, random_state=42)

    # label classification -> makes it easier to work with and save the labels
    lb = LabelBinarizer()
    trainY = lb.fit_transform(trainY)
    testY = lb.transform(testY)

    # the model used is 1200 x l2 x 10. l2 is given in FE
    model = Sequential()
    model.add(Dense(l2, input_shape=(1200,), activation="sigmoid"))
    model.add(Dense(len(lb.classes_), activation="softmax"))

    init_learning_rate = 0.01
    # Stochastic gradient descent optimizer.
    opt = SGD(lr=init_learning_rate)
    # https://peltarion.com/knowledge-center/documentation/modeling-view/build-an-ai-model/loss-functions/categorical-crossentropy
    model.compile(loss="categorical_crossentropy", optimizer=opt,
        metrics=["accuracy"])

    # train the neural network using the train sub-dataset
    H = model.fit(trainX, trainY, validation_data=(testX, testY),epochs=epochs, batch_size=batch)

    # evaluate the network using the test sub-dataset
    predictions = model.predict(testX, batch_size=32)

    # plot the training loss and accuracy
    N = np.arange(0, epochs)
    plt.style.use("ggplot")
    plt.figure()
    plt.plot(N, H.history["loss"], label="train_loss")
    plt.plot(N, H.history["val_loss"], label="val_loss")
    plt.plot(N, H.history["accuracy"], label="train_acc")
    plt.plot(N, H.history["val_accuracy"], label="val_acc")
    plt.title(f"OCR Model Performance\n\
       size: {len(data)} - batch: {batch} - test: {int(testP * 100.0)}% - epochs: {epochs} - l2: {l2}")
    plt.xlabel("Epoch")
    plt.ylabel("Loss/Accuracy")
    plt.legend()
    plt.savefig(plot_path)

    # save the model and label binarizer to disk
    model.save(model_path)
    f = open(label_path, "wb")
    f.write(pickle.dumps(lb))
    f.close()
    classification_dict = classification_report(testY.argmax(axis=1), predictions.argmax(axis=1), target_names=lb.classes_, output_dict=True)
    
    return classification_dict


def evaluate_image(image) -> dict:
    """ predicts the value of the image sent from the FE """
    flattened = image.flatten()
    reshaped = flattened.reshape((1, flattened.shape[0]))
    image = reshaped.astype("float") / 255.0

    # load the model and label binarizer
    model = load_model(model_path)
    lb = pickle.loads(open(label_path, "rb").read())

    # make a prediction on the image
    preds = model.predict(image)[0]

    # prepare a dict containing all the probabilities to be returned and displayed in the FE
    result_dict = {str(index):str(val) for index, val in enumerate(preds)}

    return result_dict
