# What is the folder?
## Load the image
> img = cv.imread("clear_rubix.jpg")
![Rubix Cube ](countour_area/rubix_center.jpg)
## convert to gray scale image
> gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
![Rubix Cube ](countour_area/rubix_grey.jpg)
## applying gaussian blur to smooth the image
> gau_blur = cv.GaussianBlur(gray_img,(3,3),0)
![Rubix Cube ](countour_area/rubix_gau_blur.jpg)
## Canny edge on smoothed image
> canny = cv.Canny(gau_blur,20,40)
![Rubix Cube ](countour_area/rubix_canny.jpg)
## writting a kernel matrix for dialation(this is not dialation step) - input is canny edge image
> dilated = cv.dilate(canny,ker, iterations=2)
