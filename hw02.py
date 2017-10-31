#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import sys

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


def run():
    """Execute program"""
    im = Image.open(sys.argv[1])
    _width, _height = im.size
    width = _width * float(sys.argv[2])
    height = _height * float(sys.argv[3])
    width = int(width)
    height = int(height)

    source = np.asarray(im)
    target = np.zeros((height, width), dtype=np.uint8)

    for y in range(height - 2):
        for x in range(width - 2):

            sx = int(min(_width - 2, math.floor(x / float(sys.argv[2]))))
            sy = int(min(_height - 2, math.floor(y / float(sys.argv[3]))))

            k = []
            i = []

            for yy in range(sy, sy + 2):
                for xx in range(sx, sx + 2):
                    i.append(source[yy][xx])
                    k.append([
                        xx, yy, xx * yy, 1
                    ])

            A = np.asarray(k)
            b = np.asarray(i)
            _x = np.linalg.solve(A, b)

            target[y][x] = int(sx * _x[0] + sy * _x[1] +
                               sx * sy * _x[2] + _x[3])

    if target.max() > 255 or target.min() < 0:
        target = 255 * ((target - target.min()) /
                        (target.max() - target.min()))

    _im = Image.fromarray(target, 'L')
    _im.show()


if __name__ == "__main__":
    # check argument count
    if len(sys.argv) < 1:
        print("usage: %s FILE WIDTH_MULTIPLIER HEIGHT_MULTIPLIER" % (sys.argv[0]))
        sys.exit()

    run()
