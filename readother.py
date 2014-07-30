import os.path
from PIL import Image 
import numpy as np

nrDataPoints = 174
imageSize = 25
emotionArray = ["google", "pi", "twitter"]
associations = {"google": "pi", "twitter": "google", "pi":"twitter"}
labelBits = imageSize**2
classLabels = {}
totHidden = 3
dataMultiplier = 2

#parse images in array bit format
def parseImage(imgName, label):
    img = Image.open(imgName)
    pixels = img.load()
    array = []
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            (a,b,c) = pixels[i,j]
            array.append((a+b+c)/3)    
    return array

def read():
	global nrDataPoints, emotionArray, dataMultiplier,classLabels, imageSize, associations
	training_datapoints = (int)(0.7 * nrDataPoints)
	data = []
	labels = []
	for i in emotionArray:
		filename = "images/" + str(associations[i])+"-image("+str(imageSize)+", "+str(imageSize)+")0.jpg"
		#print filename
		classLabels[i] = parseImage(filename, i)
	    #classLabels[i] = putLabel(i)
	    #label for each emotion will be fixed to first image in associated
	    #categori
		for j in range(training_datapoints):
			imagefile = "images/" + str(i)+"-image("+str(imageSize)+", "+str(imageSize)+")"+str(j)+".jpg"
			#print imagefile
			parsedImg = parseImage(imagefile, i)
			for m in xrange(dataMultiplier):
				data.append(parsedImg)
				labels.append(classLabels[i])
	#print data
	#print classLabels[i].shape
	return np.array(data), np.array(labels)

# read data for testing the learning
def readTest():
	global nrDataPoints, emotionArray, classLabels, dataMultiplier,imageSize, associations
	training_datapoints = (int)(0.7 * nrDataPoints)
	testing_datapoints = (int)(0.3 * nrDataPoints)
	data = []
	labels = []
	for i in emotionArray:
	    classLabels[i] = parseImage("images/" + 
	            str(associations[i])+"-image("+str(imageSize)+", "+
	            str(imageSize)+")0.jpg", i)
	    #classLabels[i] = putLabel(i)
	    #label for each emotion will be fixed to first image in associated
	    #categori
	    for j in range(training_datapoints,nrDataPoints+1):
	    	#print j
			parsedImg = parseImage("images/" + str(i)+"-image("+str(imageSize)+", "+str(imageSize)+")"+str(j)+".jpg", i)
			for m in xrange(dataMultiplier):
				data.append(parsedImg)
				labels.append(classLabels[i])
	#print data
	return np.array(data), np.array(labels)
