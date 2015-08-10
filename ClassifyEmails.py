#!bin/python

import sys
sys.path.append('liblinear-2.01/python')
from liblinearutil import *

# create labels list
labels = []
docs = []
testdocs = []
testlabels = []

def createLabels():
	f = open('training_model','r')
	for line in f:
		features = {}
		print "At line"
		params = line.rstrip().split(" ")
		labels.append(float(params[0]))
		for param in params[1:]:
			(key,val) = param.split(":")
			features[int(key)] = int(val)
		docs.append(features)

def createTestLabels():
	f = open('test_model','r')
	for line in f:
		features = {}
		params = line.rstrip().split(" ")
		testlabels.append(float(params[0]))
		for param in params[1:]:
			(key,val) = param.split(":")
			features[int(key)] = int(val)
		testdocs.append(features)

def runLiblinear():
	prob = problem(labels,docs)
	param = parameter('-c 4')
	m = train(prob,param)
	createTestLabels()
	#x0, max_idx = gen_feature_nodearray(testdocs)
	p_labs, p_acc, _ = predict(testlabels,testdocs,m)
	return p_acc

createLabels()
runLiblinear()

