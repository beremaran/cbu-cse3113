#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import datetime
from multiprocessing import Pool
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

WINDOW_SIZE = 3
k = int(WINDOW_SIZE / 2)


def equalize_histogram_local(args):
    img = args[0][args[1]:args[2], args[3]:args[4]]
    hist, bins = np.histogram(img.flatten(), 256, normed=True)
    o = hist.cumsum()
    o = 255 * o / o[-1]
    o = np.interp(img.flatten(), bins[:-1], o)
    return o.reshape(img.shape)[k, k]


def pad_img(img):
    ims = (img.shape[1], img.shape[0])
    out = np.zeros((img.shape[0] + 2 * k, img.shape[1] + 2 * k), dtype=np.uint8)
    out[k:ims[1] + k, k:ims[0] + k] = img
    return out


def run():
    source = Image.open(sys.argv[1])
    source = source.convert('L')  # convert image if it is color image
    source = np.asarray(source, dtype=np.uint8)  # convert PIL.Image to np.array
    t0 = datetime.datetime.now()
    source = pad_img(source)
    _k = k + 1
    o = []
    for y in range(k, source.shape[0] - k):
        for x in range(k, source.shape[1] - k):
            o.append((source, y - k, y + _k, x - k, x + _k))

    p = Pool(8)
    o = p.map(equalize_histogram_local, o)

    o = np.asarray(o, dtype=np.uint8)
    target = o.reshape((512, 512))
    print(datetime.datetime.now() - t0)
    Image.fromarray(target).save('140315025HW04.png')


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: 140315025HW04.py test|FILE")
        exit(1)

    run()
