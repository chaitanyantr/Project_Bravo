import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
img1 = cv.imread('template2.jpg',cv.IMREAD_GRAYSCALE)          # queryImage
vid = cv.VideoCapture(0)

while True:    
    ret, img2 = vid.read() # trainImage
    img2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
    
    # img2 = cv.imread('clutter.jpg',cv.IMREAD_GRAYSCALE) # trainImage
    # Initiate ORB detector
    orb = cv.ORB_create()
    # find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img1,None)
    kp2, des2 = orb.detectAndCompute(img2,None)

    # create BFMatcher object
    # bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=False)
       
    # Match descriptors.
    # matches = bf.match(des1,des2)
    
    matches = bf.knnMatch(des1,des2, k=2)
        
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])
    
    # Sort them in the order of their distance.
    if len(good) !=0:
        good = sorted(good, key = lambda x:x[0].distance)
    # Draw first 10 matches.
    img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,good, None, flags=2)
    
    # matches = sorted(matches, key = lambda x:x.distance)
    # img3 = cv.drawMatches(img1,kp1,img2,kp2,matches[:10],None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # plt.imshow(img3),plt.show()
    cv.imshow("output", img3)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
  
vid.release()
cv.destroyAllWindows()