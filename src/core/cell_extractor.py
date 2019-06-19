# ---------------------------------------------------
# Cells extraction using the watershed method from
# OpenCv library
# ---------------------------------------------------

import os
import time
import logging
from datetime import timedelta
from pathlib import Path

import numpy as np
from scipy import ndimage
import cv2
from skimage import morphology
from skimage import io
from skimage.measure import regionprops
from skimage.feature import peak_local_max
from core.data_manager import DataManager
from collections import namedtuple

LOW_THRESHOLD_SIZE = 1000
HIGH_THRESHOLD_SIZE = 15000


class Extractor:
    """
    Detect and extract cells from a microscope field image.

    This class have two main semantic use:
    * "batch processor mode",  process each image retrieve using a DataManager instance and extract cells
    * "prototype mode", using detect_cells and extract_cells method independently from data manager, allows
    to quickly prototyping and experimentation.
    """
    def __init__(self, data_manager):
        """

        :param data_manager: an instance of DataManager class
        """
        self.data_manager = data_manager
        self.images = self.data_manager.get_input_images()

    @staticmethod
    def detect_cells(field_image, return_steps=False):
        """

        :param field_image: a numpy ndarray instance of a 3 channel RGB image
        :param return_steps: if True a namedtuple ExtractionSteps is filled with images of algorithm step
        :return: a tuple of labels for each cell detected and namedtuple ExtractionSteps
        """
        detection_steps = namedtuple("ExtractionSteps", ["input", "meanshift",
                                                          "grayscale", "binary",
                                                          "dilation", "distance",
                                                          "labels", "filtered_labels"
                                                         ])
        # perform pyramid mean shift filtering
        # to aid the thresholding step
        shifted = cv2.pyrMeanShiftFiltering(field_image, 21, 51)

        # convert the mean shift image to grayscale, then apply
        # Otsu's thresholding
        # gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(shifted, cv2.COLOR_RGB2GRAY)
        binary = cv2.threshold(gray, 0, 255,
                                  cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        # morphological transformation
        selem = morphology.disk(5)
        dilated = morphology.dilation(binary, selem)

        # compute the exact Euclidean distance from every binary
        # pixel to the nearest zero pixel, then find peaks in this
        # distance map
        dist_map = ndimage.distance_transform_edt(dilated)
        local_max = peak_local_max(dist_map, indices=False, min_distance=20,
                                   labels=dilated)

        # perform a connected component analysis on the local peaks,
        # using 8-connectivity, then apply the Watershed algorithm
        markers = ndimage.label(local_max, structure=np.ones((3, 3)))[0]
        labels = morphology.watershed(-dist_map, markers, mask=dilated)

        # Remove labels too small and too big
        filtered_labels = np.copy(labels)
        component_sizes = np.bincount(labels.ravel())

        too_small = component_sizes < LOW_THRESHOLD_SIZE
        too_small_mask = too_small[labels]
        filtered_labels[too_small_mask] = 1

        too_big = component_sizes > HIGH_THRESHOLD_SIZE
        too_big_mask = too_big[labels]
        filtered_labels[too_big_mask] = 1

        if return_steps:
            detection_steps(input=field_image, meanshift=shifted,
                            grayscale=gray, binary=binary,
                            dilation=dilated, distance=dist_map,
                            labels=labels, filtered_labels=filtered_labels)

        return filtered_labels, detection_steps

    def extract_cells(self, field_image, cell_labels, file_name_prefix, out_path):
        """
        Given a microscope field image, extract each cell described with a label,
        cropping from the original image and save on disk as new image.

        Every cell image have a 1:1 aspect ratio and each image file name will be saved as:
         <file_name_prefix>_cell#<label_index>_<file_extension>.

        :param field_image: a numpy ndarray instance of a 3 channel RGB image
        :param cell_labels: a numpy ndarray instance of labels describing detected cells
        :param file_name_prefix: image file name's prefix string
        :param out_path: file path where cell images will be saved
        """
        regions = regionprops(cell_labels)
        export_img_extension = self.data_manager.get_output_extension()

        for i, region in enumerate(regions[1:]):  # jump the first region (regions[0]) because is the entire image

            minr, minc, maxr, maxc = region.bbox

            # Transform the region to crop from rectangular to square
            x_side = maxc - minc
            y_side = maxr - minr
            if x_side > y_side:
                maxr = x_side + minr
            else:
                maxc = y_side + minc

            if (minc > 20) & (minr > 20):
                minc = minc - 20
                minr = minr - 20

            cell = field_image[minr:maxr + 20, minc:maxc + 20]  # crop image

            # save the image
            img_name = file_name_prefix + "_cell#" + str(i) + export_img_extension
            filepath = os.path.join(out_path, img_name)
            io.imsave(filepath, cell)

            logging.info("extracted cell: {}".format(img_name))

    def batch_process(self):
        """
        Use a DataManager instance to retrieve information about images paths and for each image retrieved extract cells
        images.
        """
        logging.basicConfig(level=logging.INFO, format="[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s")

        start_time = time.monotonic()

        inpath = self.data_manager.get_input_path()
        outpath = self.data_manager.get_cells_path()

        logging.info("input path: {}".format(inpath))
        logging.info("extracted cells will be saved in: {}".format(outpath))

        if not self.images:
            logging.error("{} directory is empty! No image to process".format(inpath))

        for i, infile in enumerate(self.images):
            logging.info("detecting cells in {} image".format(infile))

            image = cv2.imread(infile)

            # transform the color scheme to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            try:
                labels, steps = self.detect_cells(image)
                self.extract_cells(image, labels, Path(infile).stem, outpath)
            except ValueError:
                continue

        end_time = time.monotonic()
        logging.info("cells extraction time: {}".format(timedelta(seconds=end_time - start_time)))


if __name__ == "__main__":
    cell_extractor = Extractor(DataManager.from_file())
    cell_extractor.batch_process()
