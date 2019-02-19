# ---------------------------------------------------
# Cells extraction using the watershed method from
# OpenCv library
# ---------------------------------------------------

# import the necessary packages
import glob
import os
import time
import numpy as np
import cv2
import configparser


from skimage import morphology
from skimage import io
from skimage.measure import regionprops
from skimage.feature import peak_local_max


from scipy import ndimage
from datetime import timedelta


def detect_cells(image):

    # perform pyramid mean shift filtering
    # to aid the thresholding step
    shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)

    # convert the mean shift image to grayscale, then apply
    # Otsu's thresholding
    # gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(shifted, cv2.COLOR_RGB2GRAY)
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # morphological transformation
    selem = morphology.disk(5)
    thresh = morphology.dilation(thresh, selem)

    # compute the exact Euclidean distance from every binary
    # pixel to the nearest zero pixel, then find peaks in this
    # distance map
    d = ndimage.distance_transform_edt(thresh)
    local_max = peak_local_max(d, indices=False, min_distance=20,
                               labels=thresh)

    # perform a connected component analysis on the local peaks,
    # using 8-connectivity, then apply the Watershed algorithm
    markers = ndimage.label(local_max, structure=np.ones((3, 3)))[0]
    labels = morphology.watershed(-d, markers, mask=thresh)
    
    # Remove labels too small and too big
    filtered_labels = np.copy(labels)
    component_sizes = np.bincount(labels.ravel())
    too_small = component_sizes < 1000
    too_small_mask = too_small[labels]
    filtered_labels[too_small_mask] = 1

    too_big = component_sizes > 15000
    too_big_mask = too_big[labels]
    filtered_labels[too_big_mask] = 1

    return filtered_labels


def extract_cells(image, image_index, out_path):

    print("Saving extracted cells in:" + out_path)
    filtered_labels = detect_cells(image)

    regions = regionprops(filtered_labels)
    for i, region in enumerate(regions[1:]): #jump the first region (regions[0]) because is the entire image

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

        cell = image[minr:maxr + 20, minc:maxc + 20]  # crop image

        filepath = os.path.join(out_path, "Img#" + str(image_index) + "_cell#" + str(i) + ".png")
        io.imsave(filepath, cell)
        print(filepath)


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read("config.ini")
    start_time = time.monotonic()

    inpath = config['Paths']['input_dir']
    outpath = config['Paths']['cells_dir']

    for i, infile in enumerate(glob.glob(os.path.join(inpath, '*.png'))):
        print(infile)

        img_or = cv2.imread(infile)

        # transform the color scheme to RGB
        img_or = cv2.cvtColor(img_or, cv2.COLOR_BGR2RGB)

        try:
            extract_cells(img_or, i, outpath)
        except ValueError:
            continue

    end_time = time.monotonic()
    print("Cell extraction time: {}".format(timedelta(seconds=end_time - start_time)))
