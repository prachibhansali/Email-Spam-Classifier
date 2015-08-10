#!bin/python
import os
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
labels = {}
labelsf = {}
trainingset = {}
testset = {}
words = {}
	
def indexEmails():
	doc_count = 0
	trainf = open('train.txt','w')
	testf = open('test.txt','w')
	f = open('trec07p/full/index')
	lab = open('labels','w')

	for line in f:
		(l,email) = line.split(" ")
		(_,_,id) = email.split("/")
		labels[id.rstrip()] = l
	scount = 0
	hcount = 0
	for file in os.listdir("trec07p/data"):
		f = open("trec07p/data/"+file,'r')
		filename = os.path.basename(file)
		print filename
		if(filename!=".DS_Store"):
			label = labels[filename]
			if(label=="spam"):
				scount = scount+1
			else : 
				hcount = hcount +1
			label = "train"

			if scount == 5:
				scount = 0
				label = "test"
			elif hcount == 5 : 
				hcount = 0
				label = "test"

			if(label=="train"):
				trainf.write(str(doc_count)+"\n")
			else:
				testf.write(str(doc_count)+"\n")

			soup = BeautifulSoup(f,'html.parser')
			es = Elasticsearch()
			doc = {
				'text' : soup.get_text(),
				'label' : labels[filename],
				'filename' : filename,
				'split' : label
			}
			res = es.index(index="email_index",doc_type="document",id=doc_count,body=doc)
			lab.write(str(doc_count) + " " + labels[filename] + "\n")
			print(res['created'])
			doc_count = doc_count + 1
	return doc_count

# scan document to get all unigrams

# read labels form file

def readLabels():
	f= open('labels','r')
	for line in f:
		(key,val) = line.split(" ")
		if(val=="spam\n"):
			labelsf[int(key)] = 0
		elif val=="ham\n":
			labelsf[int(key)] = 1

def readTrainingIds():
	train = open('train.txt','r')
	for line in train:
		trainingset[int(line.rstrip())]=True

def readTestIds():
	test = open('test.txt','r')
	for line in test:
		testset[int(line.rstrip())]=True


def fetchTrainingUnigrams():
	f = open('features','w')
	train_model = open('training_model','w')
	output = ""
	index = 0;
	for i in trainingset:
		print i
		es = Elasticsearch()
		res = es.termvector(index="email_index",doc_type="document",id=i)
		terms = res['term_vectors']['text']
		output = str(labelsf[i]) + " ";
		for key in terms['terms']:
			if key in words:
				print "found"
			else:
				words[key]=index
				f.write(key.encode('utf-8')+" "+str(index) + "\n") 
				index = index+1
			output = output + str(words[key]) +":"+str(terms['terms'][key]['term_freq']) + " "
		train_model.write(output)
		train_model.write("\n")
	print "Length of the training set "
	print len(trainingset)

def createFeatures():
	f = open('features','r')
	for line in f:
		(word,index) = line.split(" ")
		words[word] = int(index.rstrip())
	print len(words)

def createFeatureMatrixForTest():
	test_model = open('test_model','w')
	output = ""
	index = 0;
	for i in testset:
		print "test set : ",i
		es = Elasticsearch()
		res = es.termvector(index="email_index",doc_type="document",id=i)
		terms = res['term_vectors']['text']
		output = str(labelsf[i]) + " ";
		for key in terms['terms']:
			if key in words:
				output = output + str(words[key]) +":"+str(terms['terms'][key]['term_freq']) + " "
		test_model.write(output)
		test_model.write("\n")
	print "Length of the test set "
	print len(testset)



# doc_count = indexEmails()
# f = open('doccount','w')
# f.write(str(doc_count))
# f.close()
# readTrainingIds()
createFeatures()
readTestIds()
readLabels()
# fetchTrainingUnigrams()
createFeatureMatrixForTest()	




