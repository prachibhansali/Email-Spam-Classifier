#!bin/python

import sys
sys.path.append('liblinear-2.01/python')
from liblinearutil import *
from elasticsearch import Elasticsearch

# create labels list
labels = []
docs = []
testdocs = []
testlabels = []

def createLabels():
	f = open('training_model_1','r')
	for line in f:
		features = {}
		params = line.rstrip().split(" ")
		labels.append(float(params[0]))
		for param in params[1:]:
			(key,val) = param.split(":")
			features[int(key)] = float(val)
		docs.append(features)

def createTestLabels():
	f = open('test_model_1','r')
	for line in f:
		features = {}
		params = line.rstrip().split(" ")
		testlabels.append(float(params[0]))
		for param in params[1:]:
			(key,val) = param.split(":")
			features[int(key)] = float(val)
		testdocs.append(features)

def runLiblinear():
	prob = problem(labels,docs)
	param = parameter('-c 4')
	m = train(prob,param)
	createTestLabels()
	#x0, max_idx = gen_feature_nodearray(testdocs)
	p_labs, p_acc, _ = predict(testlabels,testdocs,m)
	print p_acc
	return p_labs

def printLabels(p_labs):
	f = open('labelOutputI','w')
	t = open('test.txt','r')
	lab = []
	testdata = []
	for l in p_labs:
		lab.append(l)
	for l in t:
		testdata.append(l.rstrip())
	d = {}
	for i,j in zip(lab,testdata):
		d[j] = i
	import operator
	sorted_x = sorted(d.items(),key=operator.itemgetter(1))
	output = open('output','w')
	count = 0
	for (key,val) in sorted_x:
		f.write(str(key)+" "+str(val)+ "\n")
		if count < 15:
			es = Elasticsearch()
			res = es.search(index="email_index",doc_type="document",body={"fields": ["filename","text","label"], "query": { "match": { "_id": key } } })
			result = res['hits']['hits'][0]
			#print result
			output.write(result['fields']['label'][0].encode('utf-8')+"\n"+result['fields']['filename'][0].encode('utf-8')+"\n"+result['fields']['text'][0].encode('utf-8')+"\n")
			count = count+1
	

# def getNonMatchingLabels():
# 	inf = open('incorrectlabels','w')
# 	f = open('labelOutputI','r')
# 	t = open('labels','r')
# 	cor = []
# 	incor = []
# 	for l in f:
# 		key,value = l.split(" ")
# 		incor[int(key.rstrip())]=float(value.rstrip())
# 	for l in t:
# 		key,value = l.split(" ")
# 		cor[int(key.rstrip())]=float(value.rstrip())

# 	for key,val in incor:
# 		if key in cor:
# 			if val!=cor[key]:
# 				inf.write(key+" "+val+" "+cor[key]+"\n")

createLabels()
p_labs = runLiblinear()
printLabels(p_labs)

#getNonMatchingLabels()

