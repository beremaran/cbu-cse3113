#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

'''
    Berke Emrecan Arslan <berke@beremaran.com>

    140315025
    Faculty of Engineering, Computer Science & Engineering
    Manisa Celal Bayar University

    Taken from;
    https://github.com/beremaran/cbu-cse3113
'''


def get_histogram(img):
    """Builds histogram by counting pixel intensities"""
    hist = [0] * 256
    for i in img:
        for j in i:
            hist[j] += 1
    return hist


def get_pmf(hist):
    """Calculates Probability Mass Function of a histogram"""
    pmf = [0] * 256
    total_pixels = sum(hist)
    for i in range(len(hist)):
        pmf[i] = hist[i] / total_pixels
    return pmf


def get_cdf(pmf):
    """Calculates cumulative sum of PMF data"""
    cdf = [0] * 256
    for i in range(len(pmf)):
        tmp = 0
        for j in range(i):
            tmp += pmf[j]
        cdf[i] = tmp * (256 - 1)
    return cdf


def equalize_histogram(img):
    """Equalizes histogram of numpy.array"""
    hist = get_histogram(img)
    pmf = get_pmf(hist)
    cdf = get_cdf(pmf)

    out = np.zeros_like(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            out[i][j] = cdf[img[i][j]]

    return out


def run():
    source = Image.open(sys.argv[1])
    source = source.convert('L')  # convert image if it is color image
    source.show()
    source = np.asarray(source, dtype=np.uint8)  # convert PIL.Image to np.array
    target = equalize_histogram(source)
    Image.fromarray(target).show()

    hist_src = get_histogram(source)  # histogram of source image
    hist_target = get_histogram(target)  # histogram of target image
    intensity_range = range(256)  # [0, 2^8)

    plt.figure(figsize=(20, 10))

    # source on the left
    plt.subplot(1, 2, 1)
    plt.xlabel('Intensities')
    plt.ylabel('# of pixels')
    plt.title('Histogram of the Input Image')
    plt.stem(intensity_range, hist_src, 'r-')

    # result on the right
    plt.subplot(1, 2, 2)
    plt.xlabel('Intensities')
    plt.ylabel('# of pixels')
    plt.title('Histogram of Hist. Eq. Image')
    plt.stem(intensity_range, hist_target, 'r-')

    # plt.show()
    plt.savefig('140315025HW03.png')


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: 140315025HW03.py FILE")
        exit(1)

    run()
