#!/usr/bin/env python

import argparse

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


def im_load(img_path):
    im = Image.open(img_path)
    im = im.convert('L')
    return np.asarray(im, dtype=np.uint8)


def im_center(im):
    return np.asarray(im.shape) / 2


def im_r(im, coordinates=(0, 0)):
    return np.linalg.norm(im_center(im) - coordinates)


def im_r_max(im):
    return im_r(im, np.zeros((2,)))


def im_filter(im, filter_type, filter_gain):
    r = im_r_max(im) * filter_gain
    center = im_center(im)

    y, x = np.ogrid[:im.shape[0], :im.shape[1]]

    k = 1 if filter_type == "lowpass" else -1
    return -1 * k * np.sqrt((y - center[0]) ** 2 + (x - center[1]) ** 2) >= r * k * -1


def run(img_path, filter_type="lowpass", filter_gain=0.1):
    im = im_load(img_path)

    f = np.fft.fft2(im)
    f = np.fft.fftshift(f)
    f[~im_filter(f, filter_type, filter_gain)] = 1
    f = np.fft.ifftshift(f)
    f = np.fft.ifft2(f)
    f = abs(f)

    Image.fromarray(f.astype(np.uint8)).save("140315025HW07.png", "PNG")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser("140315025HW07.py", description="Low-pass or high-pass filtering for images")
    argparser.add_argument("image_path", help="Image to be filtered")
    argparser.add_argument("filter_type", choices=["lowpass", "highpass"], help="Filter type")
    argparser.add_argument("gain", type=float, help="Filter's gain")

    args = argparser.parse_args()
    run(args.image_path, args.filter_type, args.gain)
