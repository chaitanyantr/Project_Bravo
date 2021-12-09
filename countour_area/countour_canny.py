
#Chaithanya krishna


import cv2 as cv
import numpy as np
import os
import math

cwd = os.getcwd()

img = cv.imread("clear_rubix.jpg")

hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

gau_blur = cv.GaussianBlur(gray_img,(3,3),0)

canny = cv.Canny(gau_blur,20,40)

ker = np.ones((3,3),np.uint8)

dilated = cv.dilate(canny,ker, iterations=2)

#-------------distance function----------------------------#


def calculateDistance(x1,y1,x2,y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist


#----------------------------------------------------------#

(contours, hierarchy) = cv.findContours(dilated.copy(),
                                         cv.RETR_TREE,
                                         cv.CHAIN_APPROX_SIMPLE)

print(len(contours))

candidates = []
hierarchy = hierarchy[0]

index = 0
pre_cX = 0
pre_cY = 0
center = []
rcenter = []

for component in zip(contours, hierarchy):
    contour = component[0]
    peri = cv.arcLength(contour, True)
    approx = cv.approxPolyDP(contour, 0.1 * peri, True)
    area = cv.contourArea(contour)
    corners = len(approx)

    # compute the center of the contour
    M = cv.moments(contour)

    if M["m00"]:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX = None
        cY = None

    if 1500 < area < 2000 and cX is not None:
        tmp = {'index': index, 'cx': cX, 'cy': cY, 'contour': contour}
        center.append(tmp)
        index += 1
        xy = [cX,cY]
        rcenter.append(xy)

# print(type(rcenter))


#---we have centers in rcenter,sort then to do indexing---#

print(rcenter)
#
sort_centers = sorted(rcenter , key=lambda k: [k[0], k[1]])
print(sort_centers)
sort_centers = sorted(rcenter , key=lambda k: [k[1], k[1]])
print(sort_centers)

center.sort(key=lambda k: (k.get('cy', 0)))
row1 = center[0:4]
row1.sort(key=lambda k: (k.get('cx', 0)))
row2 = center[4:8]
row2.sort(key=lambda k: (k.get('cx', 0)))
row3 = center[8:12]
row3.sort(key=lambda k: (k.get('cx', 0)))
row4 = center[12:16]
row3.sort(key=lambda k: (k.get('cx', 0)))

center.clear()
center = row1 + row2 + row3 + row4

# print(row1)

for component in center:
    candidates.append(component.get('contour'))

#-----draw circle points on image for rcenters list--#

for each_center in rcenter:
    cv.circle(img, each_center[:], 2, (255, 255, 255), -1)
#----------------------------------------------------#


#-------Red hsv----#
lower_red = np.array([130, 128, 83])
upper_red = np.array([255, 255, 1255])

#-------Orange hsv----#
lower_orange = np.array([2, 90, 50],np.uint8)
upper_orange = np.array([15, 255, 255],np.uint8)

#-------white hsv----#
lower_white = np.array([0, 0, 208])
upper_white = np.array([255, 255, 255])

#-------green hsv----#
lower_green = np.array([51, 90, 91])
upper_green = np.array([92, 255, 255])

#-------yellow hsv----#
lower_yellow = np.array([24, 17, 169])
upper_yellow = np.array([96, 214, 233])

#-------blue hsv----#
lower_blue = np.array([96, 219, 71])
upper_blue = np.array([140, 255, 213])

hsv_img = cv.cvtColor(img,cv.COLOR_BGR2HSV)

blue_frame_threshed = cv.inRange(hsv_img, lower_blue  , upper_blue)
red_frame_threshed = cv.inRange(hsv_img, lower_red, upper_red)
yellow_frame_threshed = cv.inRange(hsv_img, lower_yellow  , upper_yellow)
white_frame_threshed = cv.inRange(hsv_img, lower_white  , upper_white)
green_frame_threshed = cv.inRange(hsv_img, lower_green  , upper_green)
orange_frame_threshed = cv.inRange(hsv_img, lower_orange  , upper_orange)

# cv.imwrite('output2.jpg', blue_frame_threshed)

mask = cv.inRange(hsv_img, lower_orange, upper_orange)

cv.drawContours(img, candidates, -1, (0, 0, 255), 3)

cv.imshow("image", mask)
cv.waitKey(0)

# isWritten = cv.imwrite('rubix_center.jpg', img)
#
# if isWritten:
#     print('saved image', cwd)

