import os
import time
from useq import MDAEvent, MDASequence, Position
from pymmcore_plus.mda import mda_listeners_connected
from pymmcore_plus.mda.handlers import ImageSequenceWriter
import cv2
import numpy as np
from scipy.optimize import curve_fit
import glob

from pymmcore_plus import CMMCorePlus

core = CMMCorePlus()

f = 1192.8

def gauss(x, a, x0, sigma):
    return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

def software_autofocus(range = 20, step_size = 2):

    xx, yy = core.getXYPosition()
    z = core.getZPosition()

    # define location and type of image saving
    writer = ImageSequenceWriter(r'C:\Users\Admin\Desktop\focus', extension=".png", overwrite=True)

    # acquire z-stack
    sequence = MDASequence(
        axis_order="tpgcz",
        stage_positions=[(1200, 1214, z)],
        channels=[{'group': 'LED_light', 'config': 'on'}],
        z_plan={'above': range, 'below': range, 'step': step_size}
    )

    # run focus mda sequence
    with mda_listeners_connected(writer):
        core.mda.run(sequence)

    # calculate focus scores
    focus_images = glob.glob(r'C:\Users\Admin\Desktop\focus\*.png')
    focus_scores = []
    for f in focus_images:
        im = cv2.imread(rf'{f}')
        im_filtered = cv2.medianBlur(im, ksize=3)
        laplacian = cv2.Laplacian(im_filtered, ddepth=cv2.CV_64F, ksize=3)
        focus_score = laplacian.var()
        focus_scores.append(focus_score)

    # define x and y for fitting
    y = focus_scores
    x = np.linspace(z-range, z+range, len(y))

    # define gauss fit function
    mean = sum(x * y) / sum(y)
    sigma = np.sqrt(sum(y * (x - mean)**2) / sum(y))

    # optimize gauss fit
    popt, pcov = curve_fit(gauss, x, y, p0 = [np.max(y), mean, sigma])

    # calculate maximum focus score of fit function
    x_fine = np.linspace(z-range, z+range, 100)
    y_max = np.max(gauss(x_fine,*popt))
    pos = np.where(y_max == gauss(x_fine,*popt))
    x_max = x_fine[pos]
    y_max_data = np.max(focus_scores)
    x_max_data = x[np.where(focus_scores == y_max_data)]

    # set optimal z position
    core.setPosition(float(x_max[0]))

    # remove focus images
    for file in focus_images:
        os.remove(file)