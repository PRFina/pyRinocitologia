from skimage.measure import regionprops
import matplotlib.patches as mpatches

def add_regions_annotations(labels, axes, annotator, **kwargs):
    regions = regionprops(labels)
    for i, region in enumerate(regions[1:]):
        annotator(axes, region, i, **kwargs)


def circle_annotator(axes, region, label, **kwargs):
    x, y = region.centroid
    d = region.equivalent_diameter
    axes.add_patch(mpatches.Circle((y, x), d / 2, **kwargs))


def box_annotator(axes, region, label, **kwargs):
    xmin, ymin, xmax, ymax = region.bbox
    # Warning: the bbox coordinates are in dataspace (x are rows y are columns), rectangle is in image space (y are rows and x columns)
    bottomleft = (ymin, xmin)
    height = (xmax - xmin)
    width = (ymax - ymin)

    axes.add_patch(mpatches.Rectangle(bottomleft, width, height, **kwargs))


def label_annotator(axes, region, label, **kwargs):
    x, y = region.centroid
    d = region.equivalent_diameter
    txt = "Cell#"+str(label)
    axes.text(y, x, txt, **kwargs)
