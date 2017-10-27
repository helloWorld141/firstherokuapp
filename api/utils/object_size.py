# USAGE
# python object_size.py --image images/example_01.png --width 0.955
# python object_size.py --image images/example_02.png --width 0.955
# python object_size.py --image images/example_03.png --width 3.5

# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
# ap.add_argument("-w", "--width", type=float, required=True,
# 	help="width of the left-most object in the image (in inches)")
# ap.add_argument("-p", "--width", type=int, required=True,
# 	help="indicate whether it's front or top camera")
ap.add_argument("-a", "--objHeight", type=float, required=True,
	help="the measured height of the object")
# ap.add_argument("-s", "--camHeight", type=float, required=True,
# 	help="the height of the camera")
args = vars(ap.parse_args())
width = 122.6
# camHeight = args["camHeight"]
camHeight = 110.7
objHeight = args["objHeight"]

def process_image(imagePath, objHeight):
	width = 122.6
	camHeight = 110.7
	image = cv2.imread(imagePath)
	image = cv2.resize(image, (600, 600))
	image = image[0:400, 50:599]
	# load the image, convert it to grayscale, and blur it slightly

	# crop the image
	# image = image[0:300, 0:599]
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (7, 7), 0)

	# perform edge detection, then perform a dilation + erosion to
	# close gaps in between object edges
	edged = cv2.Canny(gray, 50, 100)
	edged = cv2.dilate(edged, None, iterations=1)
	edged = cv2.erode(edged, None, iterations=1)

	# find contours in the edge map
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	# sort the contours from left-to-right and initialize the
	# 'pixels per metric' calibration variable
	(cnts, _) = contours.sort_contours(cnts)
	pixelsPerMetric = None

	best_contour = cnts[0]	
	best_contour_area = cv2.contourArea(best_contour)

	# find the biggest contour
	for c in cnts:
		next_contour_area = cv2.contourArea(c)
		if(next_contour_area > best_contour_area):
			best_contour = c
			best_contour_area = next_contour_area 


	# loop over the contours individually
	# for c in cnts:

	# if the contour is not sufficiently large, ignore it
	# if cv2.contourArea(c) < cv2.contourArea(c) < 100:
	# 	continue


	# compute the rotated bounding box of the contour
	orig = image.copy()	
	box = cv2.minAreaRect(best_contour)
	box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
	box = np.array(box, dtype="int")



	# order the points in the contour such that they appear
	# in top-left, top-right, bottom-right, and bottom-left
	# order, then draw the outline of the rotated bounding
	# box
	box = perspective.order_points(box)


	# we will identify if the contour is rectangle or circle
	peri = cv2.arcLength(best_contour, True)
	approx = cv2.approxPolyDP(best_contour, 0.04 * peri, True)
	if(len(approx) == 4):
		print("RECTANGLE")
		# loop over the original points and draw them
		for (x, y) in box:
			cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
			cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
	else:
		print("CIRCLE")
		(x,y),radius = cv2.minEnclosingCircle(c)
		center = (int(x),int(y))
		radius = int(radius)
		cv2.drawContours(orig, [c], -1, (0, 255, 0), 2)

	# unpack the ordered bounding box, then compute thenhe midpoint
	# between the top-left and top-right coordinates, followed by
	# the midpoint between bottom-left and bottom-right coordinates
	(tl, tr, br, bl) = box
	(tltrX, tltrY) = midpoint(tl, tr)
	(blbrX, blbrY) = midpoint(bl, br)

	# compute the midpoint between the top-left and top-right points,
	# followed by the midpoint between the top-righ and bottom-right
	(tlblX, tlblY) = midpoint(tl, bl)
	(trbrX, trbrY) = midpoint(tr, br)

	# draw the midpoints on the image
	cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
	cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
	cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
	cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

	# draw lines between the midpoints
	cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
		(255, 0, 255), 2)
	cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
		(255, 0, 255), 2)

	# compute the Euclidean distance between the midpoints
	dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
	dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

	# if the pixels per metric has not been initialized, then
	# compute it as the ratio of pixels to supplied metric
	# (in this case, inches)
	# if pixelsPerMetric is None:
	# 	args["height"]
	# 	frameWidth = image.shape[1];
	# 	pixelsPerMetric = frameWidth / args["width"]
	# 	dimA = 

	# compute the size of the object

	# dimA = dA / pixelsPerMetric
	# dimB = dB / pixelsPerMetric
	dimA = dA * (camHeight - objHeight) / (objHeight)
	dimB = dB * (camHeight - objHeight) / (objHeight)

	# draw the object sizes on the image
	cv2.putText(orig, "{:.1f}in".format(dimB),
		(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (255, 255, 255), 2)
	cv2.putText(orig, "{:.1f}in".format(dimA),
		(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (255, 255, 255), 2)
	# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
	# cv2.resizeWindow('image', 600, 600)
	# show the output image
	cv2.imshow("Image", orig)
	cv2.waitKey(0)
	result = {"crop": list(box), "width": dimA, "height": dimB}
	return result

imagePath = args["image"]
process_image(imagePath, objHeight)