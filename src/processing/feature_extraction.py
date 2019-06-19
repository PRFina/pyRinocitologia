import numpy as np
import skimage.measure as skimeasure
import scipy as sci



def density(bin_img):
    bins = np.bincount(bin_img.ravel())
    npixels = bin_img.shape[0] * bin_img.shape[1]

    return bins[-1] / npixels  # for sparsity return 1-density




def clusterness(labels):
    regions = skimeasure.regionprops(labels)
    npixels = labels.shape[0] * labels.shape[1]  # number of image pixels

    centroids = [region.centroid for region in regions]
    dist_matrix = sci.spatial.distance_matrix(centroids, centroids)
    summ = 0
    total_area = 0

    for region in regions:
        dist = dist_matrix[region.label - 1].max() - dist_matrix[region.label - 1].min()
        coeff = ((region.area / npixels) * dist)
        summ += coeff
        total_area += (region.area / npixels)
        """print("id: {}, area: {}, avg dist: {}, coeff: {} ,centroid: {}".format(region.label, 
                                                                               region.area, 
                                                                               dist,
                                                                               coeff,
                                                                               region.centroid))"""
    nclusters = len(regions)
    clusterness = summ / (np.log2(nclusters) + 1)

    return clusterness, nclusters, total_area

