#from PIL import Image
import Image
from PIL import Image
import random, os, sys

''' 
for i in range(img.size[0]):    # for every pixel:
    for j in range(img.size[1]):
        pixels[i,j] = (i, j, 50) # set the colour accordingly
 '''
def genThumb(infile, size):
    outfile = os.path.splitext(infile)[0]
    if infile != outfile:
        try:
			print infile
			im = Image.open(infile)
			print "file opened"
			im.thumbnail(size, Image.ANTIALIAS)
			print outfile
			thumb = outfile + "Thumb.jpg"
			im.save(thumb)
			return thumb
        except IOError:
            print "cannot create thumbnail for '%s'" % infile

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
	if not os.path.exists("images"):
		os.makedirs("images")
	print source
	print name
	img.save("images\\" + name + ".jpg")

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
	size = (25,25) #pixels
	nrImages = 250
	trainImg = (int)(0.7 * nrImages)
	print trainImg
	source = ["smiley", "sad", "unsure"]
	source_ = ["original_images\\smiley-face-md.jpg","original_images\\sad-face-md.jpg"]
	for infile in source:
		thumb = genThumb("original_images\\"+infile+"-face-md.jpg", size)
		print thumb,"cacac"
		for i in range(trainImg):
			generateImg(6, thumb, infile+"-image"+str(size)+"%s"%i)
			#array = parseImage("smiley\\" + "smiley-image%s"%i + ".jpg")
			#print array