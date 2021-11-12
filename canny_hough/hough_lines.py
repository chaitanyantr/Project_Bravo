import cv2
import numpy as np
    
vid = cv2.VideoCapture(2)
  
while(True):      
    ret, frame = vid.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize = 3)

    lines = cv2.HoughLinesP(image=edges, rho=0.9, theta=np.pi/180, threshold=50, lines=np.array([]), minLineLength=50, maxLineGap=200)

    
    if lines is not None:
        print(lines)
        n_lines, _, _ = lines.shape
        for i in range(n_lines):
            cv2.line(frame, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 200, 255), 3, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    # cv2.imshow('edges', edges)    
      
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
vid.release()
cv2.destroyAllWindows()