import Image
from random import*
import pickle
import struct

imageSize = 30

randBinList = lambda n: [randint(0,1) for b in range(1,n+1)]
randVisState = randBinList(imageSize**2)

pixelVector = [(255,255,255) if entry==0 else (0,0,0) for entry in randVisState]
img = Image.new("RGB", (imageSize ,imageSize))
img.putdata(pixelVector)
img.save("smiley\\Output.jpg")

'''out = Image.open("smiley\\Output.jpg")
pixels = out.load()
for i in range(imageSize):
	for x in range(imageSize):
		print pixels[i,x]
		'''