import cv2
import numpy as np
    
vid = cv2.VideoCapture(-1)
  
while(True):      
    ret, frame = vid.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,12,3,0.04)

    dst = cv2.dilate(dst,None)

    frame[dst>0.01*dst.max()]=[0,0,255]

    cv2.imshow('frame', frame)
      
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
vid.release()
cv2.destroyAllWindows()