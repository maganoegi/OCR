
import cv2
# import keras
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image as pltImage
import os
import random
import math
import numpy as np 
from PIL import Image, ImageFilter
# from mnist import MNIST

# from keras.datasets import mnist
# from keras.models import Sequential, load_model
# from keras.layers.core import Dense, Dropout, Activation
# from keras.utils import np_utils

THRESHOLD = 100 # grey
SIZE = 20


def MNIST_extract(data_root, Testing=False):
    mndata = MNIST(data_root)
    images, labels = mndata.load_training() if not Testing else mndata.load_testing()
    return mndata, images, labels


def clean_MNIST(line_img):
    return np.array([x if x > THRESHOLD else 0 for x in line_img])

def print_MNIST_digit(line_img):

    print(mndata.display(line_img))
    for i in range(SIZE):
        line = ""
        for j in range(SIZE):
            line += "\033[31m█\033[0m" if line_img[i*SIZE + j] > 100 else "█"
        print(line)

def train(images, labels):
    print("\n------------------- TRAINING -------------------\n")
    (X_train, Y_train), (X_test, Y_test) = mnist.load_data()
    # building the input vector from the 28x28 pixels
    X_train = X_train.reshape(60000, 784)
    X_test = X_test.reshape(10000, 784)
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')

    # normalizing the data to help with the training
    X_train /= 255
    X_test /= 255

    print(np.unique(Y_train, return_counts=True))
    # one-hot encoding using keras' numpy-related utilities
    n_classes = 10
    print("Shape before one-hot encoding: ", Y_train.shape)
    Y_train = np_utils.to_categorical(Y_train, n_classes)
    Y_test = np_utils.to_categorical(Y_test, n_classes)
    print("Shape after one-hot encoding: ", Y_train.shape)

    # building a linear stack of layers with the sequential model
    model = Sequential()
    model.add(Dense(512, input_shape=(784,)))
    model.add(Activation('relu'))                            
    model.add(Dropout(0.2))

    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    model.add(Dense(10))
    model.add(Activation('softmax'))

    # compiling the sequential model
    model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

    # training the model and saving metrics in history
    history = model.fit(X_train, Y_train,
            batch_size=128, epochs=2,
            verbose=2,
            validation_data=(X_test, Y_test))

    # saving the model
    parentDirectory = os.path.dirname(os.path.abspath(__file__))
    save_dir = parentDirectory + "/results/"
    model_name = 'keras_mnist.h5'
    model_path = os.path.join(save_dir, model_name)
    model.save(model_path)
    print('Saved trained model at %s ' % model_path)

    mnist_model = load_model(model_path)
    loss_and_metrics = mnist_model.evaluate(X_test, Y_test, verbose=2)

    print("Test Loss", loss_and_metrics[0])
    print("Test Accuracy", loss_and_metrics[1])

    # load the model and create predictions on the test set
    mnist_model = load_model(model_path)
    print(X_test[0])
    predicted_classes = mnist_model.predict_classes(X_test)

    # see which we predicted correctly and which not
    correct_indices = np.nonzero(predicted_classes == Y_test)[0]
    incorrect_indices = np.nonzero(predicted_classes != Y_test)[0]
    print()
    print(len(correct_indices)," classified correctly")
    print(len(incorrect_indices)," classified incorrectly")


    data = MNIST_convert()
    data.astype('float32')
    print(data)
    data = data.reshape(1, 28, 28, 1)
    data = data / 255

    scores = mnist_model.predict(np.array(data))
    number = 0
    bestScore = -1
    prediction = -1
    for score in scores[0]:
        if score > bestScore:
            bestScore = score
            prediction = number

        number += 1

    print(f"prediction = {prediction} \t winner = {bestScore}")


def treat_image():

    path = './test_input.png'
    im = Image.open(path).convert('L')
    width = float(im.size[0])
    height = float(im.size[1])
    newImage = Image.new('L', (SIZE, SIZE), (255))  # creates white canvas of SIZExSIZE pixels

    if width > height:  # check which dimension is bigger
        # Width is bigger. Width becomes 20 pixels.
        nheight = int(round((20.0 / width * height), 0))  # resize height according to ratio width
        if (nheight == 0):  # rare case but minimum is 1 pixel
            nheight = 1
            # resize and sharpen
        img = im.resize((20, nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((SIZE - nheight) / 2), 0))  # calculate horizontal position
        newImage.paste(img, (4, wtop))  # paste resized image on white canvas
    else:
        # Height is bigger. Heigth becomes 20 pixels.
        nwidth = int(round((20.0 / height * width), 0))  # resize width according to ratio height
        if (nwidth == 0):  # rare case but minimum is 1 pixel
            nwidth = 1
            # resize and sharpen
        img = im.resize((nwidth, 20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((SIZE - nwidth) / 2), 0))  # caculate vertical pozition
        newImage.paste(img, (wleft, 4))  # paste resized image on white canvas


    imgArray = np.array(newImage.getdata())  # get pixel values
    
    imgArrayInv = 255 - imgArray

    imgArrayInv = clean_MNIST(imgArrayInv)

    return imgArrayInv


if __name__ == '__main__':

    # Path to Data Directory
    # parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # data_root = parentDir + "/data/"
    
    # # Extract images and labels
    # mndata, images, labels = MNIST_extract(data_root)

    # train(images, labels)


    # Display individual digit in terminal
    # index = random.randrange(0, len(images))
    # img = images[index]

    # print_MNIST_digit(img)

    # Test MNIST conversion
    data = MNIST_convert()
    # print_MNIST_digit(custom)



