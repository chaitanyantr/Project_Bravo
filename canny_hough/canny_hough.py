import numpy as np
import cv2


path = 'snapshot_640_480_2.jpg'

img = cv2.imread(path)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray,50,150,apertureSize = 3)

cv2.imwrite('edges-50-150.jpg',edges)

minLineLength=100

lines = cv2.HoughLinesP(image=edges,rho=0.7,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=minLineLength,maxLineGap=100)

a,b,c = lines.shape
for i in range(a):
    cv2.line(gray, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 200, 255), 3, cv2.LINE_AA)
    cv2.imwrite('houghlines5.jpg',gray)