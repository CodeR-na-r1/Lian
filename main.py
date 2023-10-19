import cv2 as cv
import numpy as np

import matplotlib.pyplot as plt

from Lian import LIAN

from point import Point

image = cv.imread('./map.png')
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
gray[gray > 200] = 255
gray[gray != 255] = 0

Y, X = np.loadtxt('points.txt', unpack=True)

end = Point(int(X[1]), int(Y[1]), 0)
Point.goal = end
start = Point(int(X[0]), int(Y[0]))
image = np.array(gray)

# ---- main code ----
    
path, imgMapSteps = LIAN(start, end, 10, 20, image)

plt.imshow(imgMapSteps)
plt.show()

pathImg = image.copy()
for point in path:
    pathImg = cv.circle(pathImg, (point.x, point.y), 4, (30,240,240), -1)

plt.imshow(pathImg)
plt.show()