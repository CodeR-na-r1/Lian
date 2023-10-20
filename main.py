import cv2 as cv
import numpy as np

import matplotlib.pyplot as plt

from Lian import LIAN, angle_between_vectors, angle_between_vectors2, angle_between_vectors3, angle_between_vectors4

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
    
# point1 = Point(0, 0)    # 30
# point2 = Point(2, 2)
# point3 = Point(6, 3)
# print(angle_between_vectors(point1, point2, point2, point3))
# print(angle_between_vectors2(point1, point2, point2, point3))
# print(angle_between_vectors3(point1, point2, point2, point3))
# print(angle_between_vectors4(point1, point2, point2, point3))

# point1 = Point(0, 0)    # 45
# point2 = Point(2, 0)
# point3 = Point(4, -2)
# print(angle_between_vectors(point1, point2, point2, point3))
# print(angle_between_vectors2(point1, point2, point2, point3))
# print(angle_between_vectors3(point1, point2, point2, point3))
# print(angle_between_vectors4(point1, point2, point2, point3))

# point1 = Point(0, 0)    # 45
# point2 = Point(2, 0)
# point3 = Point(1, -1)
# print(angle_between_vectors(point1, point2, point2, point3))
# print(angle_between_vectors2(point1, point2, point2, point3))
# print(angle_between_vectors3(point1, point2, point2, point3))
# print(angle_between_vectors4(point1, point2, point2, point3))

# point1 = Point(0, 0)    # 30
# point2 = Point(2, 2)
# point3 = Point(6, 3)
# print(angle_between_vectors(point1, point2, point2, point3))
# print(angle_between_vectors2(point1, point2, point2, point3))
# print(angle_between_vectors3(point1, point2, point2, point3))
# print(angle_between_vectors4(point1, point2, point2, point3))

# point1 = Point(854, 689)    # 30
# point2 = Point(874, 689)
# point3 = Point(879, 709)
# print(angle_between_vectors(point1, point2, point2, point3))
# print(angle_between_vectors2(point1, point2, point2, point3))
# print(angle_between_vectors3(point1, point2, point2, point3))
# print(angle_between_vectors4(point1, point2, point2, point3))

# params -> start, end, delta, angle, map
path, imgMapSteps = LIAN(start, end, 15, 13, image)

plt.imshow(imgMapSteps)
plt.show()

pathImg = image.copy()
for point in path:
    pathImg = cv.circle(pathImg, (point.x, point.y), 4, (30,240,240), -1)

plt.imshow(pathImg)
plt.show()