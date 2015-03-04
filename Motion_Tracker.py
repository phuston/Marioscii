import cv2
import numpy as np

class Motion_Tracker():
	""" *****Motion_Tracker****
	Uses OpenCV to find coordinates of average motion video feed from
	web camera. """

	def __init__(self):
		self.cam = cv2.VideoCapture(0)

		#BGR color boundaries for filtering out all colors except white
		self.boundaries = ([50, 30, 30], [145, 133, 128])

		ret, self.frame = self.cam.read() 
		self.init = False

	def avg_mov(self, mask):
		"""Takes in a mask, represented by a numpy array,
		outputs the x and y positions of average movement """
		# Threshold for pixels being black or white
		threshold = 250
		total_x = []
		total_y = []
		for y in xrange( mask.shape[0] ):
			for x in xrange( mask.shape[1] ):
				if mask.item(y,x) > threshold:
					total_x.append(x)
					total_y.append(y)
		return (sum(total_x)/(len(total_x)+0.1), sum(total_x)/((len(total_x))+0.1))

	def get_movement(self):
		""" Takes two frames from incoming video feed, 
		subtracts values to find areas of difference, 
		filters out all color except for white, creates
		mask that can later be used to find average areas
		of movement. """

		ret, self.frame = self.cam.read()

		# Checks if first run-through, creates last_frame
		if self.init == False:
			self.last_frame = self.frame
			ret, self.frame = self.cam.read()
			self.init = True

		frame_diff = self.frame - self.last_frame

		# Uses color boundaries to filter out all color except white
		lower, upper = self.boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")

		mask = cv2.inRange(frame_diff, lower, upper)

		# Shrink mask size to increase computational speed
		mask = cv2.pyrDown(mask)

		avg_x, avg_y = self.avg_mov(mask)

		# Last frame = current frame
		self.last_frame = self.frame

		return avg_x, avg_y


if __name__ == '__main__':
    test_tracker = Motion_Tracker()
    while True:
    	print test_tracker.get_movement()