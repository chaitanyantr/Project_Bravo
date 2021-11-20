import cv2
import numpy as np
import matplotlib as plt

vid = cv2.VideoCapture(-1)

while True:
    ret, frame = vid.read()
    img = frame
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    twoDimage = img.reshape((-1,3))
    twoDimage = np.float32(twoDimage)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 4
    attempts=1
    ret,label,center=cv2.kmeans(twoDimage,K,None,criteria,attempts,cv2.KMEANS_PP_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    result_image = res.reshape((img.shape))
    
    frame = result_image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize = 3)

    lines = cv2.HoughLinesP(image=edges, rho=0.5, theta=np.pi/180, threshold=70, lines=np.array([]), minLineLength=50, maxLineGap=200)
    
    if lines is not None:
        n_lines, _, _ = lines.shape
        for i in range(n_lines):
            cv2.line(frame, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 200, 255), 3, cv2.LINE_AA)

    cv2.imshow('frame', frame)    
    # cv2.imshow("output", result_image)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
vid.release()
cv2.destroyAllWindows()

