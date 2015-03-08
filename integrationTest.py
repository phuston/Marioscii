from AudioSampler import AudioSampler
from Motion_Tracker import Motion_Tracker

if __name__ == '__main__':

	motiontrack = Motion_Tracker()
	audiosample = AudioSampler(5000)

	while True:
		print audiosample.is_above_trigger(), motiontrack.get_movement()