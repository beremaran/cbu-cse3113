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
circle = (xx - (height / 2)) ** 2 + (yy - (width / 2))) ** 2

# Set the intensity values
for x in range(img.shape[0]):
    for y in range(img.shape[1]):
        intensity=circle[x][y]
        img[x][y]=intensity

# Display Image directly from buffer
Image.fromarray(img, 'L').show()

# Save ımage directly from buffer
Image.fromarray(img, 'L').save('circle-bad.png', 'PNG')
