import pathlib
from magicgui import magic_factory
from napari.utils.notifications import show_info
from napari.layers import Labels
from napari.types import ImageData
import numpy as np
from skimage import measure

def score_rgba(data_input, alpha):
    data_max = np.max(data_input)
    data_min = np.min(data_input)
    data_range = data_max - data_min
    ratio = 2 * (data_input-data_min) / data_range
    b = np.clip(255 * (1 - ratio), 0, 255).astype('uint8')
    r = np.clip(255 * (ratio - 1), 0, 255).astype('uint8')
    g = 255 - b - r
    b[np.where(b == 255)] = 0
    a = np.full_like(b, fill_value=alpha)
    return np.array([r, g, b, a]).T

@magic_factory(
    call_button="Load", 
    # Filter range (0-100) to remove outliers at both ends of the data distribution
    filter_min={'min': 0, 'max': 100, 'tooltip': 'Set minimum percentile to filter out lower outliers'}, 
    filter_max={'min': 0, 'max': 100, 'tooltip': 'Set maximum percentile to filter out upper outliers'}
    )
def signature_load(data_file=pathlib.Path.cwd(), filter_min: int = 1, filter_max: int = 99):
    # Note: The input data is assumed to be in CSV format with a header
    global coor, data
    raw_data = np.loadtxt(data_file, dtype="float64", delimiter=',', skiprows=1)
    coor = raw_data[:, :2].astype('int')
    data = raw_data[:, 2]
    filter_min_value = np.percentile(data, filter_min)
    filter_max_value = np.percentile(data, filter_max)
    data = np.clip(data, filter_min_value, filter_max_value)
    show_info('Successfully read file')

@magic_factory(
    auto_call=True, 
    threshold={'min': -10, 'max': 1000, 'tooltip': 'Threshold to reduce noise from low-value signals for better visualization'},
    transparency={'min': 0, 'max': 255}
    )
def signature_plot(threshold: float, transparency: int = 255) -> ImageData:
    data_result = np.clip(data, a_min=threshold, a_max=None)
    # Draw layers in the order of red, green, and blue 
    # from highest to lowest scores
    data_rgba = score_rgba(data_result, transparency)
    global signature_scores
    signature_scores = np.zeros(shape=[np.max(coor[:, 0]) + 1, np.max(coor[:, 1]) + 1, 4], dtype='uint8')
    for i in range(0, len(data)):
        signature_scores[tuple(coor[i])] = data_rgba[i]
    return ImageData(signature_scores)

@magic_factory(
    call_button="Mark", 
    threshold={'min': 0, 'max': 255, 'tooltip': 'Segmentation threshold for identifying high-intensity regions'},
    area_threshold={'min': 0, 'max': 10000, 'tooltip': 'Minimum connected region size, regions smaller than this will be ignored'}
)
def signature_segment(threshold: float, label_size: int = 100, name: str = "Signature Labels") -> Labels:
    # Convert RGBA image to grayscale for binarization, 
    # with red having the highest weight and blue the lowest
    signature_grayscale = 0.7 * signature_scores[:, :, 0] + 0.2 * signature_scores[:, :, 1] + 0.1 * signature_scores[:, :, 2]
    binary = signature_grayscale > threshold
    # Label connected regions
    labels = np.array(measure.label(binary))
    # Remove regions smaller than minimum size
    props = measure.regionprops(labels)
    for prop in props:
        if prop.area < label_size:
            labels[labels == prop.label] = 0
    labels = np.array(measure.label(labels > 0))
    # Draw labels
    result = np.zeros(shape=[np.max(coor[:, 0]) + 1, np.max(coor[:, 1]) + 1], dtype='uint32')
    for i in range(len(data)):
        result[coor[i, 0], coor[i, 1]] = labels[coor[i, 0], coor[i, 1]]
        
    return Labels(result, name=name)
