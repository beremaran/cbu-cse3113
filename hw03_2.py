#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

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


def equalize_histogram(img):
    """Equalizes histogram of numpy.array"""
    hist, bins = np.histogram(img.flatten(), 256, normed=True)
    o = hist.cumsum()
    o = 255 * o / o[-1]
    o = np.interp(img.flatten(), bins[:-1], o)
    return o.reshape(img.shape)


def run():
    source = Image.open(sys.argv[1])
    source = source.convert('L')  # convert image if it is color image
    source = np.asarray(source, dtype=np.uint8)  # convert PIL.Image to np.array
    target = equalize_histogram(source)

    hist_src = np.histogram(source.flatten(), 256, normed=True)[0]  # histogram of source image
    hist_target = np.histogram(target.flatten(), 256, normed=True)[0]  # histogram of target image
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
