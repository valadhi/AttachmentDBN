import Image
import random, os

''' 
for i in range(img.size[0]):    # for every pixel:
    for j in range(img.size[1]):
        pixels[i,j] = (i, j, 50) # set the colour accordingly
 '''

def generateImg(diffusionRate, source, name):
	img = Image.open(source)
	pixels = img.load() # create the pixel map
	imglen = img.size[0]
	imgwid = img.size[1]
	for i in range(diffusionRate):
		#choose random pixel locations
		x = random.randint(0, imglen-1)
		y = random.randint(0, imgwid-1)
		x_= random.randint(0, imglen-1)
		y_= random.randint(0, imgwid-1)
		#swap pixels
		a = pixels[x,y]
		pixels[x,y] = pixels[x_, y_]
		pixels[x_, y_] = a
	if not os.path.exists("sad"):
		os.makedirs("sad")
	img.save("sad\\" + name + ".jpg")

def parseImage(imgName):
	img = Image.open(imgName)
	pixels = img.load()
	array = []
	for i in range(img.size[0]):
		for j in range(img.size[1]):
			(a,b,c) = pixels[i,j]
			if a > 200:#if pixel "blackness" is over 200
				array.append(0)
			else:
				array.append(1)
	return array
				

if __name__ == '__main__':
	nrImages = 10
	dataset = set()
	source = "sad-face.jpg"
	for i in range(nrImages):
		generateImg(8, source, "sad-image%s"%i)
		array = parseImage("sad\\" + "sad-image%s"%i + ".jpg")
		print array