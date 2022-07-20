import wave, struct, math, random, numpy as np
points = [-i**7/5040 + i**5/120 - i**3/6 + i for i in range(-200,200)]
def normalise(x, offset=0, r_min=min(points), r_max=max(points), t_min=-32894, t_max=32894):
	#x = (x + offset) % r_max
	normalised_x = (x - r_min) / (r_max - r_min)  #* (t_max - t_min) + t_min
	return normalised_x




sampleRate = 44100.0 # hertz
duration = 1.0 # seconds
frequency = 440.0 # hertz
obj = wave.open('sound.wav','w')
obj.setnchannels(1) # mono
obj.setsampwidth(2)
obj.setframerate(sampleRate)
for i in range(-200,200):
   value = math.floor(-i**7/5040 + i**5/120 - i**3/6 + i)
   print(value)
   data = struct.pack('<h', value)
   obj.writeframesraw( data )
obj.close()



# import wave
# import numpy as np
# import sys
# import matplotlib.pyplot as plt

# channels = 2
# framerate = 44100
# samplewidth = 16 * 8
# nframes = 100

# f =  wave.open('test_file.wav', mode='wb')
# f.setparams((channels,samplewidth,framerate,nframes, None, 'None'))
# music = bytes.fromhex('2Ef0 F1f2  ')
# f.writeframes(music)
# f.close()


##(nchannels, sampwidth, framerate, nframes, comptype, compname)