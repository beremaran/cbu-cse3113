#!/usr/bin/env python
#-*- coding: utf-8 -*-

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

## ==

'''
    Print 'circle' object before next code block. Values exceeds 8-bit unsigned
integer limits. So we need to map values of "circle" matrix to range of:
    [0, 256)

Simple example for mapping:

    MAPPED_VALUE = VALUE * (TARGET_RANGE_MAX / CURRENT_RANGE_MAX)

Let's say that we want to map "6" from [0, 10] to [0, 100]:

    x = 6 * (100 / 10)
    x = 60

If source or target range is not starting from zero, check map() function from
Arduino libraries:

    https://www.arduino.cc/en/Reference/Map (see Appendix)
'''

circle *= 255.0 / circle.max()
## ==

# Set the intensity values
for x in range(img.shape[0]):
    for y in range(img.shape[1]):
        intensity = circle[x][y]
        img[x][y] = intensity

# Display Image directly from buffer
Image.fromarray(img, 'L').show()

# Save ımage directly from buffer
Image.fromarray(img, 'L').save('circle-bad.png', 'PNG')
