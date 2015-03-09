import alsaaudio
import audioop
import time

class AudioSampler:
	def __init__(self, trigger_vol):
		self.trigger_vol = trigger_vol
		self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,0)
		self.inp.setchannels(1)
		self.inp.setrate(5000) # Sets sampling rate to 8000 Hz
		self.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
		self.inp.setperiodsize(200)
		# self.inp.setperiodsize(160)

	def get_level(self):
		l,data = self.inp.read()
		if l and audioop.rms(data,2) > self.trigger_vol:
				return audioop.rms(data,2)
		else:
			return None

	def is_above_trigger(self):
		l,data = self.inp.read()
		if l:
			if audioop.rms(data,2) > self.trigger_vol:
				return True
			else: 
				return False
		return False


if __name__ == '__main__':
	audiosampler = AudioSampler(3000)
	while True:
		print audiosampler.get_level()