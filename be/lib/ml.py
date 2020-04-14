


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

if __name__ == "__main__":
        
    this_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(this_dir)


    dataset_path = os.path.join(base_path, "digits")
    model_path = os.path.join(base_path, "model", "digit_nn.model")
    label_path = os.path.join(base_path, "model", "digit_nn_lb.pickle")
    plot_path = os.path.join(base_path, "model", "digit_nn_plot.png")
    test_path = os.path.join(base_path, "test_images")


    # initialize the data and labels
    print("[INFO] loading images...")
    data = []
    labels = []
    # grab the image paths and randomly shuffle them
    imagePaths = sorted(list(paths.list_images(dataset_path)))
    random.seed(42)
    random.shuffle(imagePaths)
    # loop over the input images
    for imagePath in imagePaths:
        # load the image, resize the image to be 32x32 pixels (ignoring
        # aspect ratio), flatten the image into 32x32x3=3072 pixel image
        # into a list, and store the image in the data list
        image = cv2.imread(imagePath).flatten()
        # TODO: Sanity Check dimentions
        data.append(image)
        # extract the class label from the image path and update the
        # labels list
        label = imagePath.split(os.path.sep)[-2]
        labels.append(label)

    # scale the raw pixel intensities to the range [0, 1]
    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)

    # partition the data into training and testing splits using 75% of
    # the data for training and the remaining 25% for testing
    (trainX, testX, trainY, testY) = train_test_split(data,
        labels, test_size=0.25, random_state=42)

    # convert the labels from integers to vectors (for 2-class, binary
    # classification you should use Keras' to_categorical function
    # instead as the scikit-learn's LabelBinarizer will not return a
    # vector)
    lb = LabelBinarizer()
    trainY = lb.fit_transform(trainY)
    testY = lb.transform(testY)


    # define the 3072-1024-512-3 architecture using Keras
    model = Sequential()
    model.add(Dense(1024, input_shape=(1200,), activation="sigmoid"))
    model.add(Dense(512, activation="sigmoid"))
    model.add(Dense(len(lb.classes_), activation="softmax"))

    # initialize our initial learning rate and # of epochs to train for
    INIT_LR = 0.01
    EPOCHS = 75
    # compile the model using SGD as our optimizer and categorical
    # cross-entropy loss (you'll want to use binary_crossentropy
    # for 2-class classification)
    print("[INFO] training network...")
    opt = SGD(lr=INIT_LR)
    model.compile(loss="categorical_crossentropy", optimizer=opt,
        metrics=["accuracy"])

    # train the neural network
    H = model.fit(trainX, trainY, validation_data=(testX, testY),
        epochs=EPOCHS, batch_size=6)

    # evaluate the network
    print("[INFO] evaluating network...")
    predictions = model.predict(testX, batch_size=32)
    print(classification_report(testY.argmax(axis=1),
        predictions.argmax(axis=1), target_names=lb.classes_))
    # plot the training loss and accuracy
    N = np.arange(0, EPOCHS)
    plt.style.use("ggplot")
    plt.figure()
    plt.plot(N, H.history["loss"], label="train_loss")
    plt.plot(N, H.history["val_loss"], label="val_loss")
    plt.plot(N, H.history["accuracy"], label="train_acc")
    plt.plot(N, H.history["val_accuracy"], label="val_acc")
    plt.title("Training Loss and Accuracy (Platonov OCR)")
    plt.xlabel("Epoch")
    plt.ylabel("Loss/Accuracy")
    plt.legend()
    plt.savefig(plot_path)

    # save the model and label binarizer to disk
    print("[INFO] serializing network and label binarizer...")
    model.save(model_path)
    f = open(label_path, "wb")
    f.write(pickle.dumps(lb))
    f.close()

    for index in range(10):

        target_digit = str(index)
        image_name = target_digit + ".png"
        test_image_path = os.path.join(test_path, image_name)
        image = cv2.imread(test_image_path).flatten()
        image = image.reshape((1, image.shape[0]))
        # output = image.copy()
        # image = cv2.resize(image, (20, 20))
        # scale the pixel values to [0, 1]
        image = image.astype("float") / 255.0
        # load the model and label binarizer
        model = load_model(model_path)
        lb = pickle.loads(open(label_path, "rb").read())
        # make a prediction on the image
        preds = model.predict(image)
        # find the class label index with the largest corresponding
        # probability
        res = preds.argmax(axis=1)[0]
        label = lb.classes_[res]
        for i in range(10):
            this_one = i == res
            winner = res == int(target_digit)
            color = ""
            end = ""
            if this_one:
                end = "'\x1b[0m'"
                color = '\x1b[6;30;42m' if winner else '\x1b[6;30;41m'
                print(f"{i}:\t{color}{preds[0][i]}{end}")

        print(f"Expected result: {target_digit}\tObtained result: {res}")
        print("================================================================")