
#Chaithanya krishna
import cv2 as cv
import numpy as np
import os

cwd = os.getcwd()

img = cv.imread("clear_rubix.jpg")

gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

gau_blur = cv.GaussianBlur(gray_img,(3,3),0)

canny = cv.Canny(gau_blur,20,40)

ker = np.ones((3,3),np.uint8)

dilated = cv.dilate(canny,ker, iterations=2)

#---------------------------------------------------------#

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
for component in zip(contours, hierarchy):
    contour = component[0]
    peri = cv.arcLength(contour, True)
    approx = cv.approxPolyDP(contour, 0.1 * peri, True)
    area = cv.contourArea(contour)
    corners = len(approx)

    # compute the center of the contour
    M = cv.moments(contour)

    # print('M',M)
    print('M["m00"]',M["m00"])

    if M["m00"]:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX = None
        cY = None

    if 1500 < area < 10000 and cX is not None:
        tmp = {'index': index, 'cx': cX, 'cy': cY, 'contour': contour}
        center.append(tmp)
        index += 1

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

for component in center:
    candidates.append(component.get('contour'))

cv.drawContours(img, candidates, -1, (0, 0, 255), 3)
cv.imshow("image", img)
cv.waitKey(0)













isWritten = cv.imwrite('countour.jpg', dilated)

if isWritten:
    print('saved image', cwd)

cv.imshow("Image", dilated)
cv.waitKey(0)
cv.destroyAllWindows()