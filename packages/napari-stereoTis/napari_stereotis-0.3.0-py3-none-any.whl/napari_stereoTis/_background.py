from magicgui import magic_factory
from napari.layers import Image, Labels
import numpy as np
import cv2
import pathlib

def rgb2rgba(img, alpha):
    img_rgba = np.empty(shape=[img.shape[0], img.shape[1], 4], dtype='uint8')
    if len(img.shape) == 2:
        # 将灰度图像的像素值复制到RGB图像的每个颜色通道中。
        # 这意味着灰度图像的值被复制到红、绿、蓝三个通道中，形成一个伪RGB图像。
        for channel in range(0, 3):
            img_rgba[:, :, channel] = img
    else:
        img_rgba[:, :, 0:3] = img
    img_rgba[:, :, 3] = alpha
    return img_rgba

@magic_factory(call_button="Background", transparency={'min': 0, 'max': 255})
def input_background(filename=pathlib.Path.cwd(), transparency: int = 255) -> Image:
    # 通常情况下，显式地将 pathlib.Path 对象转换为字符串是一个好的做法，以确鲁棒性。
    bk_img = cv2.imread(str(filename))
    # 将BGR转换为RGB
    if bk_img is not None and len(bk_img.shape) == 3:
        bk_img = cv2.cvtColor(bk_img, cv2.COLOR_BGR2RGB)
    bk_img_rgba = rgb2rgba(bk_img, transparency)
    return Image(bk_img_rgba, name="Background", blending='translucent')

@magic_factory(call_button="Cells Masks", transparency={'min': 0, 'max': 255})
def input_cells(filename=pathlib.Path.cwd(), transparency: int = 150) -> Labels:
    if str(filename).endswith('_seg.npy'):
        cells = np.load(filename, allow_pickle=True).item()
        label_array = cells['masks']
    else:
        # 提前检查array需不需要转置
        label_array = np.load(filename)
    return Labels(label_array, name="Cells")

@magic_factory(call_button="Nucleus Masks", transparency={'min': 0, 'max': 255})
def input_nucleus(filename=pathlib.Path.cwd(), transparency: int = 150) -> Labels:
    if str(filename).endswith('_seg.npy'):
        cells = np.load(filename, allow_pickle=True).item()
        label_array = cells['masks']
    else:
        # 提前检查array需不需要转置
        label_array = np.load(filename)
    return Labels(label_array, name="Nucleus")

@magic_factory(call_button="Cytoplasm Masks", transparency={'min': 0, 'max': 255})
def input_cytoplasm(filename=pathlib.Path.cwd(), transparency: int = 150) -> Labels:  
    if str(filename).endswith('_seg.npy'):
        cells = np.load(filename, allow_pickle=True).item()
        label_array = cells['masks']
    else:
        # 提前检查array需不需要转置
        label_array = np.load(filename)
    return Labels(label_array, name="Cytoplasm")