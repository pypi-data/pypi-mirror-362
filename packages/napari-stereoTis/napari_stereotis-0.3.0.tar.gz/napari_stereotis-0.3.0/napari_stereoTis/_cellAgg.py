from magicgui import magic_factory
from napari.utils.notifications import show_info
from napari.layers import Image, Labels
from napari.types import LabelsData
from enum import Enum
import numpy as np
import cv2
import pathlib
from sklearn import cluster

def coor2array(coor):
    imarray = np.zeros([max(coor[:, 0]) + 1, max(coor[:, 1]) + 1], dtype='uint8')
    if coor.shape[1] == 3:
        for coor_pair in coor:
            imarray[coor_pair[0], coor_pair[1]] = coor_pair[2]
    else:
        for coor_pair in coor:
            imarray[coor_pair[0], coor_pair[1]] = 255
    return imarray

def cls2array(cls_coor, labels):
    cls_data = np.column_stack((cls_coor, labels+1))
    cls_img = coor2array(cls_data)
    return cls_img

def rgb2rgba(img, alpha):
    img_rgba = np.empty(shape=[img.shape[0], img.shape[1], 4], dtype='uint8')
    if len(img.shape) == 2:
        for channel in range(0, 3):
            img_rgba[:, :, channel] = img
    else:
        img_rgba[:, :, 0:3] = img
    img_rgba[:, :, 3] = alpha
    return img_rgba

class EpsType(Enum):
    x5 = 0.05
    x10 = 0.1
    x15 = 0.15
    x20 = 0.2

@magic_factory(call_button="Load", transparency={'min': 0, 'max': 255})
def cells_load(filename=pathlib.Path.cwd(), transparency: int = 150, name: str = "Cells Aggregates") -> Image:
    # The input data is assumed to be in CSV format with a header
    # with the first column as x-coordinates, the second column as y-coordinates
    global data
    data = np.loadtxt(filename, delimiter=",", skiprows=1).astype(int)
    raw_img = coor2array(data)
    raw_img_rgba = rgb2rgba(raw_img, transparency)
    return Image(raw_img_rgba, name=name)

@magic_factory(
    call_button="OPTICS", 
    min_samples={'min': 2, 'max': 100},
    tooltip={'tooltip': "OPTICS clustering based on the minimum samples and reachability/xi . The xi is generally used with its default value (x5: 0.05)."}
)
def cls_optics(xi=EpsType.x5, min_samples: int = 8) -> Labels:
    xi_value = xi.value
    clustering = cluster.OPTICS(min_samples=min_samples,xi=xi_value).fit(data)
    cls_img = cls2array(data, clustering.labels_)
    imgname = "OPTICS_" + str(min_samples)
    show_info(str(max(clustering.labels_)) + ' cluster in total')
    return Labels(cls_img, name=imgname)

@magic_factory(
    call_button="Optimize", 
    kernel_size={'min': 1, 'max': 5, 'tooltip': 'Kernel size for morphological closing operations'}, 
    area_threshold={'min': 0, 'max': 10000, 'tooltip': 'Minimum region size, regions smaller than this will be ignored'}
    )
def cls_optimize(img_layer: LabelsData, kernel_size: int = 3, area_threshold: int = 20) -> LabelsData:
    """
    Perform morphological closing operation on labeled clusters and 
    filterring clusters based on their area size.
    Args:
        img_layer: Input labeled image data
        kernel_size: Size of the structuring element for morphological operations
        area_threshold: Minimum area size to keep (in pixels)
    Returns:
        Processed image with closed clusters
    """
    img_data = img_layer
    # Create rectangular structuring element for morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    cls_layer = np.zeros_like(img_data, dtype='uint8')
    cls_size = {}
    
    # Process each cluster separately
    for n_cluster in range(1, np.max(img_data)+1):
        # Create binary mask for current cluster
        cluster_img = np.zeros_like(img_data, dtype='uint8')
        cluster_img[np.where(img_data == n_cluster)] = 255
        # Apply morphological closing
        cluster_img_close = cv2.morphologyEx(np.array(cluster_img, dtype=np.uint8), cv2.MORPH_CLOSE, kernel)
        # Find and draw contours
        contours, _ = cv2.findContours(cluster_img_close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        blank_img = np.uint8(np.full(cluster_img_close.shape, 0))
        rst = cv2.drawContours(np.array(blank_img.copy(), dtype=np.uint8), contours, -1, (int(n_cluster),), -1)
        # Add to cls_layer and calculate cluster size
        cls_layer += rst
        cls_size[n_cluster] = np.sum(rst != 0)

    cls_area = cls_layer.copy()
    # filterring cluster by area
    for label, area in cls_size.items():
        if area < area_threshold:
            cls_area[np.where(cls_area == label)] = 0
    # Relabel remaining clusters to make labels continuous, excluding 0
    remaining_labels = np.unique(cls_area)[1:]
    # Get elements and their indices simultaneously, starting index from 1
    for new_label, old_label in enumerate(remaining_labels, 1):
        cls_area[cls_area == old_label] = new_label
            
    return LabelsData(cls_area)
