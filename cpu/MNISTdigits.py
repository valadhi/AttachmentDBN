""" This module is manily created to test the deep belief and
rbm implementations on MNIST"""

import argparse
import matplotlib.pyplot as plt
import numpy as np
import cPickle as pickle
import readmnist
import readsmiley
import restrictedBoltzmannMachine as rbm
import deepbelief as db
import utils
#import PCA
import PIL
import glob

#import DimensionalityReduction

from common import *

parser = argparse.ArgumentParser(description='RBM for digit recognition')
parser.add_argument('--save',dest='save',action='store_true', default=False,
                    help="if true, the network is serialized and saved")
parser.add_argument('--train',dest='train',action='store_true', default=False,
                    help=("if true, the network is trained from scratch from the"
                          "traning data"))
parser.add_argument('--pca', dest='pca',action='store_true', default=False,
                    help=("if true, the code for running PCA on the data is run"))
parser.add_argument('--rbm', dest='rbm',action='store_true', default=False,
                    help=("if true, the code for traning an rbm on the data is run"))
parser.add_argument('--rbmPCD', dest='rbmPCD',action='store_true', default=False,
                    help=("if true, the code for traning an rbm on the data is run"))
parser.add_argument('--db', dest='db',action='store_true', default=False,
                    help=("if true, the code for traning a deepbelief net on the"
                          "data is run"))
parser.add_argument('--trainSize', type=int, default=10000,
                    help='the number of tranining cases to be considered')
parser.add_argument('--testSize', type=int, default=1000,
                    help='the number of testing cases to be considered')
parser.add_argument('netFile', help="file where the serialized network should be saved")


# Get the arguments of the program
args = parser.parse_args()

def visualizeWeights(weights, imgShape, tileShape):
  return utils.tile_raster_images(weights, imgShape,
                                  tileShape, tile_spacing=(1, 1))

def rbmMain(reconstructRandom=False):
  '''
  trainVectors, trainLabels =\
      readmnist.read(0, args.trainSize, digits=None, bTrain=True, path="MNIST")
  #print trainVectors.shape
  testingVectors, testLabels =\
      readmnist.read(0, args.testSize, digits=None, bTrain=False, path="MNIST")
  '''
  trainVectors, trainLabels =\
      readsmiley.read()
  testingVectors, testLabels =\
      readsmiley.readTest()

  print "trainVectors",trainVectors.shape," trainLabels", trainLabels.shape
  print "testingVectors",testingVectors.shape," testLabels", testLabels.shape
  reconstructTuple = (40, 20)

  trainvect = np.concatenate((trainVectors, trainLabels), axis=1)
  testvect = np.concatenate((testingVectors, testLabels), axis=1)

  print "trainvect",trainvect.shape," testvect", testvect.shape

  trainingScaledVectors = trainvect/ 255.0
  testingScaledVectors = testvect/ 255.0
  #print "a",len(testingScaledVectors)

  # Train the network
  if args.train:
    # The number of hidden units is taken from a deep learning tutorial
    # The data are the values of the images have to be normalized before being
    # presented to the network
    nrVisible = len(trainingScaledVectors[0])
    nrHidden = 500
    # use 1 dropout to test the rbm for now
    net = rbm.RBM(nrVisible, nrHidden, rbm.contrastiveDivergence, 1, 1)
    net.train(trainingScaledVectors)
    t = visualizeWeights(net.weights.T, reconstructTuple, (10,10))
  else:
    # Take the saved network and use that for reconstructions
    f = open(args.netFile, "rb")
    t = pickle.load(f)
    net = pickle.load(f)
    f.close()

  rando = np.random.random_sample(testingVectors[0,:].shape)
  # Reconstruct an image and see that it actually looks like a digit
  threshold = len(testLabels) /len(emotionArray)
  label1 = label1.reshape(1, label1.shape[0])
  label2 = label2.reshape(1, label2.shape[0])
  label3 = label3.reshape(1, label3.shape[0])
  rando = rando.reshape(1, rando.shape[0])

  recon1 = net.reconstruct(rando, label1,3)
  recon2 = net.reconstruct(rando, label2,3)
  recon3 = net.reconstruct(rando, label3,3)
  recon11 = net.reconstruct(rando, label1,300)
  recon21 = net.reconstruct(rando, label2,300)
  recon31 = net.reconstruct(rando, label3,300)
  saveImage(recon1, "1")
  saveImage(recon2, "2")
  saveImage(recon3, "3")
  saveImage(recon11, "11")
  saveImage(recon21, "21")
  saveImage(recon31, "31")


  # get a random image and see how it looks like
#  if reconstructRandom:
#    rando = np.random.random_sample(label.shape)


  print test.shape
  plt.imshow(vectorToImage(test, (40,20)), cmap=plt.cm.gray)
  plt.savefig('paste.png', transparent=False)
  plt.imshow(vectorToImage(test, reconstructTuple), cmap=plt.cm.gray)
  plt.show()

  # Show the reconstruction
  recon = net.reconstruct(test.reshape(1, test.shape[0]))
  plt.imshow(vectorToImage(recon, reconstructTuple), cmap=plt.cm.gray)
  plt.axis('off')
  plt.savefig('12.png', transparent=True)
  # plt.show()
  
  # Make label reconstruction
  #emrecon = net.reconstructLabel()

  # Show the weights and their form in a tile fashion
  # Plot the weights
  plt.imshow(t, cmap=plt.cm.gray)
  plt.axis('off')
  plt.savefig('weights.png', transparent=True)

  print "done"

  if args.save:     
    f = open(args.netFile, "wb")
    pickle.dump(t, f)
    pickle.dump(net, f)

def savetrain(datatrain, t):
  print "asdfadsfwaefw",datatrain.shape
  for i in xrange(3):
    plt.imshow(vectorToImage(datatrain[i,:], (50, 25)), cmap=plt.cm.gray)
    plt.axis('off')
    plt.savefig("trainingimg/"+str(t*i)+".png",transparent=True)

def saveImage(data, name):
  plt.imshow(vectorToImage(data, (50, 25)), cmap=plt.cm.gray)
  plt.axis('off')
  plt.savefig(name + '.png',transparent=True)  

def rbmMainPCD():
  emotionArray = ["unsure", "smiley", "sad"]
  associations = {"unsure": "smiley", "sad": "unsure", "smiley":"sad"}
  reconstructTuple = (50, 25)
  nrData = 175

  '''trainVectors, trainLabels =\
      readmnist.read(0, args.trainSize, digits=None, bTrain=True, path="MNIST")
  testingVectors, testLabels =\
      readmnist.read(0, args.testSize, digits=None,bTrain=False, path="MNIST")
'''
  # use custom read method for smiley faces
  trainVectors, trainLabels = readsmiley.read()
  testingVectors, testLabels = readsmiley.readTest()
  print "trainVectors",trainVectors.shape," trainLabels", trainLabels.shape
  print "testingVectors",testingVectors.shape," testLabels", testLabels.shape

  #shuffle the data
  #trainVectors, trainLabels = shuffle(trainVectors, trainLabels)
  #testingVectors, testLabels = shuffle(testingVectors, testLabels)

  # normalize vectors
  trainVectors = trainVectors / 255.0
  trainLabels = trainLabels / 255.0
  testingVectors = testingVectors / 255.0
  testLabels = testLabels / 255.0

  # concatenate train and label image into a training set
  trainingScaledVectors = np.concatenate((trainVectors, trainLabels), axis=1)
  testingScaledVectors = np.concatenate((testingVectors, testLabels), axis=1)
  print "trainvect",trainingScaledVectors.shape," testvect", testingScaledVectors.shape

  np.random.shuffle(trainingScaledVectors)
  savetrain(trainingScaledVectors, nrData)
  # Train the network
  if args.train:
    # The number of hidden units is taken from a deep learning tutorial
    # The data are the values of the images have to be normalized before being
    # presented to the network
    nrVisible = len(trainingScaledVectors[0])
    nrHidden = 500
    # use 1 dropout to test the rbm for now
    # net = rbm.RBM(nrVisible, nrHidden, rbm.contrastiveDivergence, 1, 1)
    net = rbm.RBM(nrVisible, nrHidden, rbm.PCD, 1, 1)
    net.train(trainingScaledVectors)
    t = visualizeWeights(net.weights.T, reconstructTuple, (10,10))
  else:
    # Take the saved network and use that for reconstructions
    f = open(args.netFile, "rb")
    t = pickle.load(f)
    net = pickle.load(f)
    f.close()

  # Reconstruct a training image and see that it actually looks like a digit
  threshold = len(testLabels) /len(emotionArray)
  label1 = testLabels[0*threshold,:]
  label2 = testLabels[1*threshold,:]
  label3 = testLabels[2*threshold,:]
  #print "labels",label
  plt.imshow(vectorToImage(label1, (25,25)), cmap=plt.cm.gray)
  plt.savefig('label1.png', transparent=True)
  rando = np.random.random_sample(testingVectors[0,:].shape)
  
  test = np.concatenate((rando, label1), axis=1)
  plt.imshow(vectorToImage(test, reconstructTuple), cmap=plt.cm.gray)
  plt.savefig('random.png', transparent=True)

  # reshape data and label
  label1 = label1.reshape(1, label1.shape[0])
  label2 = label2.reshape(1, label2.shape[0])
  label3 = label3.reshape(1, label3.shape[0])
  rando = rando.reshape(1, rando.shape[0])

  recon1 = net.reconstruct(rando, label1,3)
  recon2 = net.reconstruct(rando, label2,3)
  recon3 = net.reconstruct(rando, label3,3)
  recon11 = net.reconstruct(rando, label1,300)
  recon21 = net.reconstruct(rando, label2,300)
  recon31 = net.reconstruct(rando, label3,300)
  saveImage(recon1, "1")
  saveImage(recon2, "2")
  saveImage(recon3, "3")
  saveImage(recon11, "11")
  saveImage(recon21, "21")
  saveImage(recon31, "31")

  # Show the weights and their form in a tile fashion
  plt.imshow(t, cmap=plt.cm.gray)
  plt.axis('off')
  plt.savefig('weightsPCDall.png',transparent=True)

  print "done"

  if args.save:
    f = open(args.netFile, "wb")
    pickle.dump(t, f)
    pickle.dump(net, f)


def shuffle(data, labels):
  indexShuffle = np.random.permutation(len(data))
  shuffledData = np.array([data[i] for i in indexShuffle])
  shuffledLabels = np.array([labels[i] for i in indexShuffle])

  return shuffledData, shuffledLabels

'''
def pcaOnMnist(training, dimension=700):
  principalComponents = PCA.pca(training, dimension)
  low, same = PCA.reduce(principalComponents, training)

  image2DInitial = vectorToImage(training[0], (28,28))
  print same[0].shape
  image2D = vectorToImage(same[0], (28,28))

  plt.imshow(image2DInitial, cmap=plt.cm.gray)
  plt.show()
  plt.imshow(image2D, cmap=plt.cm.gray)
  plt.show()
  print "done"
'''

def deepbeliefMNIST():
  training = args.trainSize
  testing = args.testSize

  trainVectors, trainLabels =\
      readmnist.read(0, training, bTrain=True, path="MNIST")
  testVectors, testLabels =\
      readmnist.read(0, testing, bTrain=False, path="MNIST")
  print trainVectors[0].shape

  trainVectors, trainLabels = shuffle(trainVectors, trainLabels)

  trainingScaledVectors = trainVectors / 255.0
  testingScaledVectors = testVectors / 255.0

  vectorLabels = labelsToVectors(trainLabels, 10)

  if args.train:
    # net = db.DBN(3, [784, 500, 10], [Sigmoid(), Softmax()])
    # net = db.DBN(4, [784, 500, 500, 10], [Sigmoid, Sigmoid, Softmax])

    net = db.DBN(5, [784, 1000, 1000, 1000, 10],
                 [Sigmoid, Sigmoid, Sigmoid, Softmax],
                 dropout=0.5, rbmDropout=0.5, visibleDropout=0.8,
                 rbmVisibleDropout=1)
    # TODO: think about what the network should do for 2 layers
    net.train(trainingScaledVectors, vectorLabels)
  else:
    # Take the saved network and use that for reconstructions
    f = open(args.netFile, "rb")
    net = pickle.load(f)
    f.close()


  probs, predicted = net.classify(testingScaledVectors)
  correct = 0
  for i in xrange(testing):
    print "predicted"
    print "probs"
    print probs[i]
    print predicted[i]
    print "actual"
    actual = testLabels[i]
    print actual
    correct += (predicted[i] == actual)

  print "correct"
  print correct

  # for w in net.weights:
  #   print w

  # for b in net.biases:
  #   print b


  # t = visualizeWeights(net.weights[0].T, trainImages[0].(28, 28), (10,10))
  # plt.imshow(t, cmap=plt.cm.gray)
  # plt.show()
  # print "done"

  if args.save:
    f = open(args.netFile, "wb")
    pickle.dump(net, f)
    f.close()

"""
  Arguments:
    big: should the big or small images be used?
    folds: which folds should be used (1,..5) (a list). If None is passed all
    folds are used
"""
def deepBeliefKanade(big=False, folds=None):
  if big:
    files = glob.glob('kanade_150*.pickle')
  else:
    files = glob.glob('kanade_f*.pickle')

  if not folds:
    folds = range(1, 6)

  # Read the data from them. Sort out the files that do not have
  # the folds that we want
  # TODO: do this better (with regex in the file name)
  # DO not reply on the order returned
  files = files[folds]

  data = []
  labels = []
  for filename in files:
    with open(filename, "rb") as  f:
      # Sort out the labels from the data
      dataAndLabels = pickle.load(f)
      foldData = dataAndLabels[0:-1 ,:]
      foldLabels = dataAndLabels[-1,:]
      data.append(foldData)
      labels.append(foldLabels)

  # Do LDA

  # Create the network

  # Test

  # You can also group the emotions into positive and negative to see
  # if you can get better results (probably yes)
  pass

'''
# TODO: fix this (look at the ML coursework for it)
# Even better, use LDA
# think of normalizing them to 0.1 for pca as well
def pcaMain():
  training = args.trainSize
  testing = args.testSize

  train, trainLabels =\
      readmnist.read(0, training, bTrain=True, path="MNIST")
  testVectors, testLabels =\
      readmnist.read(0, testing, bTrain=False, path="MNIST")
  print train[0].shape

  pcaOnMnist(train, dimension=100)
'''
def main():
  if args.db + args.pca + args.rbm + args.rbmPCD != 1:
    raise Exception("You decide on one main method to run")

  if args.db:
    deepbeliefMNIST()
  #if args.pca:
  #  pcaMain()
  if args.rbmPCD:
    rbmMainPCD()
  if args.rbm:
    rbmMain()


if __name__ == '__main__':
  main()
