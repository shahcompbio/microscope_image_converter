import os
import skimage
import skimage.io
import numpy as np
from matplotlib import pyplot as plt


def convert(red_path, cyan_path, output_path):
    red = skimage.io.imread(red_path)
    red_adj = skimage.exposure.rescale_intensity(red, out_range=(0,255)).astype('uint8')

    cyan = skimage.io.imread(cyan_path)
    cyan_adj = skimage.exposure.rescale_intensity(cyan, out_range=(0,255)).astype('uint8')

    zero_array = np.zeros(cyan_adj.shape).astype('uint8')

    reshaped = np.dstack((red_adj, cyan_adj, zero_array))

    skimage.io.imsave(output_path, reshaped, format='png')

