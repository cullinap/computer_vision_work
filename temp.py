# import the necessary packages
import numpy as np
import imutils
import cv2


def main():

	filename = 'images/board_game.png'
	W = 300	
	img = cv2.imread(filename, cv2.IMREAD_COLOR)
	height, width, depth = img.shape
	imgscale = W/width
	newX, newY = img.shape[1]*imgscale, img.shape[0]*imgscale
	new_img = cv2.resize(img, (int(newX), int(newY)))
	
	cv2.imshow("Show by CV2",new_img)
	cv2.waitKey(0)
	cv2.imwrite('images/board_game_sm.png',new_img)

if __name__ == '__main__':
	main()