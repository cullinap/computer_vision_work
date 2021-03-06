# USAGE
# python detect_barcode.py --image images/barcode_01.jpg

# import the necessary packages
import numpy as np
import argparse
import imutils
import cv2

def main():

	filename = 'images/barcode_sm.jpg'
	W = 300	
	img = cv2.imread(filename, cv2.IMREAD_COLOR)
	height, width, depth = img.shape
	imgscale = W/width
	newX, newY = img.shape[1]*imgscale, img.shape[0]*imgscale
	new_img = cv2.resize(img, (int(newX), int(newY)))
	
	# cv2.imshow("Show by CV2",new_img)
	# cv2.waitKey(0)
	# cv2.imwrite("resizeimg.jpg",new_img)

	# cv2.destroyAllWindows()

	gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
	# compute the Scharr gradient magnitude representation of the images
	# in both the x and y direction using OpenCV 2.4
	ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
	gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
	gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)
	# subtract the y-gradient from the x-gradient
	gradient = cv2.subtract(gradX, gradY)
	gradient = cv2.convertScaleAbs(gradient)
	# cv2.imshow("Show by CV2",gradient)
	# cv2.waitKey(0)

	blurred = cv2.blur(gradient, (9, 9))
	(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

	# construct a closing kernel and apply it to the thresholded image
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
	closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

	# perform a series of erosions and dilations
	closed = cv2.erode(closed, None, iterations = 4)
	closed = cv2.dilate(closed, None, iterations = 4)

	# find the contours in the thresholded image, then sort the contours
	# by their area, keeping only the largest one
	cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
	# compute the rotated bounding box of the largest contour
	rect = cv2.minAreaRect(c)
	box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
	box = np.int0(box)
	# draw a bounding box arounded the detected barcode and display the
	# image
	cv2.drawContours(new_img, [box], -1, (0, 255, 0), 3)
	cv2.imshow("Image", new_img)
	cv2.imwrite("images/barcode_sm_edge.jpg",new_img)
	cv2.waitKey(0)


if __name__ == '__main__':
	main()









