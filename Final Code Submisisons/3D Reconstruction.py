
#Chaithanya krishna & Mithulesh Ramkumar


import cv2 as cv
import numpy as np
import os
import math
from numpy.lib.utils import info
from pandas import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D





def getdilated(img):
    
    cwd = os.getcwd()


    hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    gau_blur = cv.GaussianBlur(gray_img,(3,3),0)

    canny = cv.Canny(gau_blur,20,40)

    ker = np.ones((3,3),np.uint8)

    dilated = cv.dilate(canny,ker, iterations=2)
    
    return dilated

#-------------distance function----------------------------#


def calculateDistance(x1,y1,x2,y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist


#----------------------------------------------------------#

def getcountours(dilated):
    (contours, hierarchy) = cv.findContours(dilated.copy(),
                                            cv.RETR_TREE,
                                            cv.CHAIN_APPROX_SIMPLE)
    return contours,hierarchy




# print(len(contours))
def getrcenter(hierarchy,contours):
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
            
    return rcenter,center
     

# print(type(rcenter))


#---we have centers in rcenter,sort then to do indexing---#


#

def getindex(rcenter,center):
    
    candidates = []
    sort_centers = sorted(rcenter , key=lambda k: [k[0], k[1]])


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

    # Indexing
    col1 = sort_centers[0:4]
    col2 = sort_centers[4:8]
    col3 = sort_centers[8:12]
    col4 = sort_centers[12:16]

    sort_col1 = sorted(col1 , key=lambda k: [k[1], k[1]])
    sort_col2 = sorted(col2 , key=lambda k: [k[1], k[1]])
    sort_col3 = sorted(col3 , key=lambda k: [k[1], k[1]])
    sort_col4 = sorted(col4 , key=lambda k: [k[1], k[1]])

    a = 2
    b = 4
    c = 4

    rubiks_lst = [[ ['#' for col in range(a)] for col in range(b)] for row in range(c)]


    rubiks_lst[0][0] = sort_col1[0]
    rubiks_lst[1][0] = sort_col1[1]
    rubiks_lst[2][0] = sort_col1[2]
    rubiks_lst[3][0] = sort_col1[3]
    rubiks_lst[0][1] = sort_col2[0]
    rubiks_lst[1][1] = sort_col2[1]
    rubiks_lst[2][1] = sort_col2[2]
    rubiks_lst[3][1] = sort_col2[3]
    rubiks_lst[0][2] = sort_col3[0]
    rubiks_lst[1][2] = sort_col3[1]
    rubiks_lst[2][2] = sort_col3[2]
    rubiks_lst[3][2] = sort_col3[3]
    rubiks_lst[0][3] = sort_col4[0]
    rubiks_lst[1][3] = sort_col4[1]
    rubiks_lst[2][3] = sort_col4[2]
    rubiks_lst[3][3] = sort_col4[3]




    pretty_list = DataFrame(rubiks_lst)


    print(pretty_list)
    
    for component in center:
        candidates.append(component.get('contour'))

    #-----draw circle points on image for rcenters list--#

    
    
    return pretty_list,rubiks_lst





# print(sort_col1)
# print(col1)



def gethsvranges(img):

    hsv_img = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    
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

    blue_frame_threshed = cv.inRange(hsv_img, lower_blue  , upper_blue)
    red_frame_threshed = cv.inRange(hsv_img, lower_red, upper_red)
    yellow_frame_threshed = cv.inRange(hsv_img, lower_yellow  , upper_yellow)
    white_frame_threshed = cv.inRange(hsv_img, lower_white  , upper_white)
    green_frame_threshed = cv.inRange(hsv_img, lower_green  , upper_green)
    orange_frame_threshed = cv.inRange(hsv_img, lower_orange  , upper_orange)
    
    return blue_frame_threshed,red_frame_threshed,yellow_frame_threshed,white_frame_threshed,green_frame_threshed,orange_frame_threshed


# Main Function
def main():
    print("Hello World!")
    
    img = cv.imread("clear_rubix.jpg")    
    dilated = getdilated(img)
    
    contours,hierarchy = getcountours(dilated)
    rcenter,center = getrcenter(hierarchy,contours)
    
    index,rubiks_lst = getindex(rcenter,center)
    
    blue_frame_threshed,red_frame_threshed,yellow_frame_threshed,white_frame_threshed,green_frame_threshed,orange_frame_threshed = gethsvranges(img)


    i = 4

    # Create axis
    axes = [4, 4, 4]

   # Create Data
    data = np.ones(axes, dtype=np.bool)

    # Tranperency
    alpha = 0.9
    


    # control colour 
    colors = np.ones(axes + [4], dtype=np.float32)
    colors[0] = [0, 0, 0, alpha] # Black
    colors[1] = [0, 0, 0, alpha] # Black
    colors[2] = [0, 0, 0, alpha] # Black
    colors[3] = [0, 0, 0, alpha] # Black



    # for each_center in rcenter:
    #     cv.circle(img, each_center[:], 2, (255, 255, 255), -1)
        
   
    cv.waitKey(0)
    
    
    for x in range(0,i):
        for y in range(0,i):
            index_x = rubiks_lst[x][y][0]
            index_y = rubiks_lst[x][y][1]
            if orange_frame_threshed[index_y+5][index_x+5] == 255:
                x_temp = x
                if x == 0:
                    x_temp = 3
                if x == 1:
                    x_temp = 2
                if x == 2:
                    x_temp = 1
                if x == 3:
                    x_temp = 0
                colors[0][x_temp][y] =  [1, 0.65, 0, alpha] # Orange
                
            if blue_frame_threshed[index_y+5][index_x+5] == 255:
                x_temp = x
                if x == 0:
                    x_temp = 3
                if x == 1:
                    x_temp = 2
                if x == 2:
                    x_temp = 1
                if x == 3:
                    x_temp = 0
                colors[0][x_temp][y] =  [0, 0, 1, alpha] # blue
            
            if red_frame_threshed[index_y+5][index_x+5] == 255:
                x_temp = x
                if x == 0:
                    x_temp = 3
                if x == 1:
                    x_temp = 2
                if x == 2:
                    x_temp = 1
                if x == 3:
                    x_temp = 0
                colors[0][x_temp][y] =  [1, 0, 0, alpha] # red
            
            if yellow_frame_threshed[index_y+5][index_x+5] == 255:
                x_temp = x
                if x == 0:
                    x_temp = 3
                if x == 1:
                    x_temp = 2
                if x == 2:
                    x_temp = 1
                if x == 3:
                    x_temp = 0
                colors[0][x_temp][y] =  [1, 1, 0, alpha] # yellow
            
            if white_frame_threshed[index_y+5][index_x+5] == 255:
                x_temp = x
                if x == 0:
                    x_temp = 3
                if x == 1:
                    x_temp = 2
                if x == 2:
                    x_temp = 1
                if x == 3:
                    x_temp = 0
                colors[0][x_temp][y] =  [1, 1, 1, alpha] # White
            
            if green_frame_threshed[index_y+5][index_x+5] == 255:
                x_temp = x
                if x == 0:
                    x_temp = 3
                if x == 1:
                    x_temp = 2
                if x == 2:
                    x_temp = 1
                if x == 3:
                    x_temp = 0
                colors[0][x_temp][y] =  [0, 0.5, 0, alpha] # green
            


    



    # cv.drawContours(img, candidates, -1, (0, 0, 255), 3)

   
    cv.waitKey(0)

    # Creating 3D Rubiks Cube
    # https://www.geeksforgeeks.org/how-to-draw-3d-cube-using-matplotlib-in-python/
    
    
    # Plot figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Voxels is used to customizations of the 
    # sizes, positions and colors.
    ax.voxels(data, facecolors=colors, edgecolors='grey')

    plt.show()

    




    

if __name__ == "__main__":
    main()


