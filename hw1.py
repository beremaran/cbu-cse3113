#!/usr/bin/env python
#-*- coding: utf-8 -*-

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

import numpy as np
from PIL import Image

# Image size
width = 600
height = 400

# Create an empty image
img = np.zeros((height, width), dtype=np.uint8)

# Create [x, y] coordinate combinations on grid
xx, yy = np.mgrid[:height, :width]
# Mathematical definition of a circle centered at (200,300)
circle = (xx - (height / 2)) ** 2 + (yy - (width / 2)) ** 2

# ==

'''
    Print 'circle' object before next code block. Values exceeds 8-bit unsigned
integer limits, called 'overflow', So we need to map (normalize) values of
`circle` matrix to range of:
    [0, 256)

## Simple example for normalizing
(assuming both of ranges have a start value of 0)

    MAPPED_VALUE = VALUE * (TARGET_RANGE_MAX / CURRENT_RANGE_MAX)

Let's say that we want to map "6" from [0, 10] to [0, 100]:

    x = 6 * (100 / 10)
    x = 60

If source or target range is not starting from zero, check map() function from
Arduino libraries:

    https://www.arduino.cc/en/Reference/Map (see Appendix)
'''

circle *= 255.0 / circle.max()
# ==

# Set the intensity values
for x in range(img.shape[0]):
    for y in range(img.shape[1]):
        intensity = circle[x][y]
        img[x][y] = intensity

# Display Image directly from buffer
Image.fromarray(img, 'L').show()

# Save ımage directly from buffer
Image.fromarray(img, 'L').save('circle-bad.png', 'PNG')
