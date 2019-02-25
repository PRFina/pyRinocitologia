# Import libraries and modules
import cv2
import os
from os import path
import numpy as np
import shutil
import configparser

from keras.models import load_model

# TODO: eplace with config. file

def get_class_path(classNum, config):
    # convert the cell-class number into its name string.
    if classNum == 0:
        return config["Paths"]["epiteliali_dir"]
    if classNum == 1:
        return config["Paths"]["neutrofili_dir"]
    if classNum == 2:
        return config["Paths"]["eosinofili_dir"]
    if classNum == 3:
        return config["Paths"]["mastcellule_dir"]
    if classNum == 4:
        return config["Paths"]["linfociti_dir"]
    if classNum == 5:
        return config["Paths"]["mucipare_dir"]
    if classNum == 6:
        return config["Paths"]["others_dir"]


def load_resize_img(img_path):

    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return cv2.resize(img, (50, 50))


def load_data(cell_directory):

    """
    Loading images and labels from cell directory
    :param cell_directory: directory path with extracted cell images
    :return: images, image'names
    """
    file_names = [path.join(cell_directory, img_name) for img_name in os.listdir(cell_directory)
                  if img_name.endswith('.png') or img_name.endswith('.PNG')]
    images = [load_resize_img(img_name) for img_name in file_names]

    return images, file_names


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    # load the trained model.
    model = load_model(config["Models"]["classifier"])
    model.load_weights(config["Models"]["classifier_weights"])
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy')

    # load cell images
    images, file_names = load_data(config["Paths"]["cells_dir"])

    # TODO: review the code below, use skimage functions to convert and optimize the code
    # images to multi dimensional arrays
    images = np.array(images)
    images = images.astype("float32")
    images /= 255
    images = images.reshape(images.shape[0], 50, 50, 3)

    out_path = config["Paths"]["output_dir"]

    for i, (img, img_name) in enumerate(zip(images, file_names)):
        img = img.reshape((1,)+img.shape)
        # add a dimension to the image
        img_class = model.predict_classes(img)

        # define the path of its folder-class (classify the image).
        class_path = get_class_path(img_class, config)

        # move it to the correct destination.
        shutil.move(img_name, class_path)
        print("Predict class for image {}: {}".format(file_names[i], class_path))
