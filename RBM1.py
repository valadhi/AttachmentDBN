'''
RBM Unit
'''
import Image
import numpy as np
import pickle
from random import *
import os.path
import struct
epsilon = 0.000001

nrDataPoints = 30
imageSize = 30
emotionArray = ["smiley", "sad"]
labelBits = 10
classLabels = {}
totHidden = 5

def sigmoid(v):
    return 1/(1+np.exp(-v))

def hidden_activation_probability(v, W, c):
    activations = np.zeros(W.shape[0])
    #print "hidden_activation_probability: " +str(W.shape) + str(c.shape) + str(len(v))
    for i in range(W.shape[0]):
        activations[i] = sigmoid(c[i] + sum([W[i,j]*v[j] for j in range(W.shape[1])]))
    return activations

def visible_activation_probability(h,W,b):
    activations = np.zeros(W.shape[1])
    #print "visible_activation_probability: " +str(W.shape) + str(b.shape) + str(len(h))
    for j in range(W.shape[1]):
        activations[j] = sigmoid(b[j] + sum([W[i,j]*h[i] for i in range(W.shape[0])]))
    return activations

def sample_hidden_state(v,W,c):
    #print "sample_hidden_state: " +str(W.shape) + str(c.shape) + str(len(v))
    hidden_probabilities = hidden_activation_probability(v,W,c)
    return np.random.uniform(size=hidden_probabilities.shape) < hidden_probabilities

def sample_vis_state(v,W,c):
    #print "sample_vis_state: " +str(W.shape) + str(c.shape) + str(len(v))
    visible_probabilities = visible_activation_probability(v,W,c)
    return np.random.uniform(size=visible_probabilities.shape) < visible_probabilities

def rbmUpdate(x,W,b,c,lr=0.1):
    h1 = sample_hidden_state(x,W,c)
    v2 = sample_vis_state(h1,W,b)
    q_v2 = visible_activation_probability(h1,W,b)
    q_h2 = hidden_activation_probability(v2,W,c)
    new_b = b + lr*(x-v2)
    new_c = c + lr*(h1-q_h2)
    a = np.outer(h1,x)
    b = np.outer(q_h2,v2.T)
    new_W = W + lr*(a-b)
    error = np.sum(np.sum((x-q_v2)**2))
    return new_W,new_b,new_c,error

#def rbmLabelUpdate():

class RBM(object):
    def __init__(self, visible_units, hidden_units):
        self.v = visible_units
        self.h = hidden_units
        self.W = np.random.random(size=(hidden_units, visible_units))
        self.b = np.random.random(visible_units)
        self.c = np.random.random(hidden_units)

    def train(self, data, lr=0.05, max_iterations=1000, eps=0.1):
        iteration = 0
        last_error = eps+1
        while iteration < max_iterations and last_error > eps:
            for item in data:
                self.W,self.b,self.c,last_error = rbmUpdate(item, self.W,self.b,self.c,lr)
            iteration += 1
            if iteration % 10 == 0:
                print last_error
                #print self.W[1,-10:]
                #print self.W[1,-10:]

def softmaxlabel(weights, layr):
    global labelBits
    label = np.zeros(labelBits)
    prob = label
    sumx_i = 0
    x_i = []
    for i in xrange(labelBits):
        x_i.append(np.exp(sum([weights[j,-labelBits] * layr[j] 
            for j in xrange(weights.shape[0])]))) 
        sumx_i += x_i[i]

    prob = [x_i[i]/sumx_i for i in xrange(labelBits)]
    r = np.random.random()
    indx = 0
    while(r>=0 and indx<labelBits):
        r -= prob[indx]
        indx+=1
    label[indx-1] = 1
    #print label
    return label.tolist()

#parse images in array bit format
def parseImage(imgName, label):
    img = Image.open(imgName)
    pixels = img.load()
    array = []
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            (a,b,c) = pixels[i,j]
            if a > 200 and b>200 and c>200:#if pixel "blackness" is over 200
                array.append(0)
            else:
                array.append(1)      
    return array

def createData():
    global nrDataPoints, emotionArray, classLabels
    training_datapoints = (int)(0.7 * nrDataPoints)
    data = []
    label = []
    for i in emotionArray:
        classLabels[i] = softmaxlabel(np.zeros((2,900)), np.zeros(900))
        #label = softmaxlabel(np.zeros((2,900)), np.zeros(900))
        for j in range(training_datapoints):
            parsedImg = parseImage(str(i) + "\\" + str(i)+
                "-image"+str(j)+".jpg", i)
            data.append(parsedImg + classLabels[i])

    print classLabels
    return data

def CD_1Label(vis, Wght, c, b):
    global labelBits
    label = vis[-labelBits:]
    h_smple = sample_hidden_state(vis, Wght, c)
    sample = sample_vis_state(h_smple,Wght,b)
    #replace label part of array
    sample[-labelBits:] = label
    return sample

def createImagefromWeights(data, hidden_unit_nr, emotion, gen):
    global imageSize, emotionArray, labelBits, classLabels, totHidden
    # TODO method to extract variables from data
    tothu = totHidden #total nr hidden units
    ia = imageSize**2 # size of one image array
    ila = imageSize**2 + labelBits # image and label array size
    W = data[hidden_unit_nr:hidden_unit_nr+1,0:ila]
    c = data[hidden_unit_nr:hidden_unit_nr+1,ila]
    b = data[tothu,0:ila]

    randBinList = lambda n: [randint(0,1) for b in range(1,n+1)]
    randVisState = randBinList(imageSize**2)
    #attach label bit to end of random string
    '''if(emotion == "sad"):
        randVisState.extend([0,0,0,0,0,1,0,0,0,0])
    elif(emotion == "smiley"):
        randVisState.extend([0,0,0,0,0,0,0,0,0,1])'''

    randVisState.extend(classLabels[emotion])
    #print emotion
    vect_ = CD_1Label(randVisState, W, c, b)
    ###### run 4 steps of CD
    for caca in range(20):
        vect = CD_1Label(vect_.tolist(), W, c, b)
        #print type(vect),"vect",vect.shape
        vect_ = CD_1Label(vect.tolist(), W, c, b)

    pixelVector_ = CD_1Label(vect_.tolist(), W, c, b)
    #print h1.shape,"h1"
    #pixelVector_ = sample_vis_state(h1,W,b)
    pixelVector_ = pixelVector_[:-labelBits]
    #print pixelVector_.shape

    pixelVector = [(255,255,255) if entry==False else (0,0,0) for entry in pixelVector_]
    img = Image.new("RGB", (imageSize ,imageSize))
    img.putdata(pixelVector)
    img = img.rotate(-90)
    img.save(emotion + "\\Outputsoftmax"+str(gen)+".jpg")

def start():
    global imageSize, emotionArray, labelBits, classLabels, totHidden
    tempWeights = "LogisticWeights"
    tempLabels = "LogisticLabels"

    if(os.path.isfile(tempWeights) and os.path.isfile(tempLabels)): 
        # previously created weights found
        print "file Found"
        with open(tempWeights, 'rb') as f:
            data = pickle.load(f)
        with open(tempLabels, 'rb') as g:
            classLabels = pickle.load(g)
        #print classLabels
        #print "e" + str(data.shape)
        for i in range(len(emotionArray)):
            for j in range(13):
                createImagefromWeights(data, i, emotionArray[i], j)
    else:
        if(os.path.isfile(tempWeights) or os.path.isfile(tempLabels)):
            print "Files are missing"
        else:
            # create RBM with (imageSize + labelBits) visible units
            # and length of emotionArray hidden units
            training_data = createData()
            r = RBM(imageSize**2 + labelBits, totHidden)
            r.train(training_data ,max_iterations=100,lr=0.1)
            data_ = np.concatenate((r.W, np.array([r.c]).T), axis = 1)
            #print r.W.shape
            print "data saved: " + str(data_.shape)
            #visible bias needs 1 bit of padding to concatenate
            r.b = np.insert(r.b, imageSize**2-1, 0)
            print "b: " + str(np.array([r.b]).shape)
            data = np.concatenate((data_, np.array([r.b])), axis = 0)

            with open(tempWeights, 'wb') as f:
                pickle.dump(data, f)
            with open(tempLabels, 'wb') as g:
                pickle.dump(classLabels, g)
            #createImagefromWeights(np.array([[r.W], [r.c]]), 0)
  
start()

#TODO: make number of visible units corelated to number of pixels in image