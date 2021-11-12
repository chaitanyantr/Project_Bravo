# Chaithanya krishna

import cv2 as cv
import numpy as np
import os

img = cv.imread("rubix_cropped.jpg", cv.IMREAD_GRAYSCALE)

cwd = os.getcwd()

# print('directory',cwd)
#
sift_features = cv.xfeatures2d.SIFT_create()

key_points, image_descriptor = sift_features.detectAndCompute(img, None)

img = cv.drawKeypoints(img, key_points, None)

isWritten = cv.imwrite('sift_output.jpg', img)

if isWritten:
    print('saved image', cwd)

cv.imshow("Image", img)
cv.waitKey(0)
cv.destroyAllWindows()
