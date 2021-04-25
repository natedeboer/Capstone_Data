#Run code with: $python3 motion_measurement.py -v [video_name]

from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
cursurface = 0
vs = cv2.VideoCapture(args["video"])

firstFrame = None

j = 0
numFrames = 0;
avg = 0
while True:
	numFrames += 1
	j = j+1
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]
	text = "Unoccupied"
	if frame is None:
		break

	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	if j == 15:
		firstFrame = gray
		j = 0
		continue
	if firstFrame is None:
		firstFrame = gray
		continue

	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	surface = 500 * 372
	for c in cnts:
		cursurface += cv2.contourArea(c)
	avg += (cursurface*100)/surface
	cursurface = 0
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

print("Total Movement: ",avg)
avg = avg / numFrames
print("Average Movement per Frame: ",avg)
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
