import numpy as np
import skimage.morphology as skimorph
import skimage.measure as skimeasure
import cv2 as cv2


def binarization(img):
    img = cv2.pyrMeanShiftFiltering(img, 10, 20)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    binary = skimorph.dilation(binary, skimorph.disk(5))

    return binary


def filter_labels(labels, min_area=500, max_area=None):
    filtered = labels.copy()

    min_area_mask = np.bincount(labels.ravel()) < min_area  # get area for each label and filter
    mask = min_area_mask[filtered]
    filtered[mask] = 0  # set as background label

    if max_area:
        max_area_mask = np.bincount(labels.ravel()) > max_area  # get area for each label and filter
        mask = max_area_mask[filtered]
        filtered[mask] = 0

    return skimeasure.label(filtered)  ## recompute labels to restart ids
