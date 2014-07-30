import RBMCDLabel as rbm

nrDataPoints = 30
imageSize = 30
emotionArray = ["smiley", "sad"]

def createData():
    global nrDataPoints, emotionArray
    training_datapoints = (int)(0.7 * nrDataPoints)
    data = []
    label = []
    for i in emotionArray:
        #classLabels[i] = softmaxlabel(np.zeros((2,900)), np.zeros(900))
        #label = softmaxlabel(np.zeros((2,900)), np.zeros(900))
        for j in range(training_datapoints):
            parsedImg = parseImage(str(i) + "\\" + str(i)+
                "-image"+str(j)+".jpg", i)
            data.append(parsedImg)
    return data

class DBN(object):

	def _init(self, nrLayers, LayerSize):

	def trainLayers(self, data, labels=None):
		layer = rbm.RBM(900, 2)
		layer.train()

