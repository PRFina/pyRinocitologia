
import shutil
import configparser
import skimage
from core.data_manager import DataManager
from keras.models import load_model


class Classifier:

    INPUT_IMAGE_WIDTH = 50
    INPUT_IMAGE_HEIGHT = 50

    def __init__(self, config_file, data_mngr):

        config = configparser.ConfigParser()
        config.read(config_file)

        # load the trained model.
        self.model = load_model(config["Models"]["classifier"])
        self.model.load_weights(config["Models"]["classifier_weights"])
        self.model.compile(optimizer='rmsprop', loss='categorical_crossentropy')

        self.data_manager = data_mngr

    @staticmethod
    def pre_process_image(img_path):
        """
        Apply image transformations to adapt input images to model input
        :param img_path:
        :return:
        """
        img = skimage.io.imread(img_path)
        img = skimage.img_as_float32(img)
        img = skimage.transform.resize(img, (Classifier.INPUT_IMAGE_WIDTH, Classifier.INPUT_IMAGE_HEIGHT))

        return img.reshape((1,) + img.shape)  # add one dimension, needed for keras conv2d input layer

    def load_images(self):

        """
        Utility method to load cells images and apply pre-transformations
        :return: list of tuples: (image RGB ndarray, image file name)
        """

        file_names = self.data_manager.get_cells_images()
        images = [Classifier.pre_process_image(img_name) for img_name in file_names]

        return images, file_names

    def classify(self, cell_image, cell_image_name):

        img = cell_image
        img_class = self.model.predict_classes(img)

        # define the path of its folder-class (classify the image).
        class_path = self.data_manager.get_cell_class_path(img_class[0])

        # move it to the correct destination.
        shutil.move(cell_image_name, class_path)

        return img_class[0]

    def batch_process(self):

        # load cell images
        images, file_names = self.load_images()

        for i, (img, img_name) in enumerate(zip(images, file_names)):
            cell_class = self.classify(img, img_name)
            print("Predict class for image {}: {}".format(file_names[i], self.data_manager.get_cell_class_path(cell_class)))


if __name__ == "__main__":
    classifier = Classifier("config.ini", DataManager.from_file())
    classifier.batch_process()
