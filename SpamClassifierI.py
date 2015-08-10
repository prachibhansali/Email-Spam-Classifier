#!bin/python

from elasticsearch import Elasticsearch

spamwords = {}
featureMatrix = {}
trainingset = {}
testset = {}
labelsf = {}

def readSpamWords():
	f = open('SpamWords','r')
	for line in f:
		spamwords[line.rstrip()] = True

def readTrainingIds():
	train = open('train.txt','r')
	for line in train:
		trainingset[int(line.rstrip())]=True

def readTestIds():
	test = open('test.txt','r')
	for line in test:
		testset[int(line.rstrip())]=True

def readLabels():
	f= open('labels','r')
	for line in f:
		(key,val) = line.split(" ")
		if(val=="spam\n"):
			labelsf[int(key)] = 0
		elif val=="ham\n":
			labelsf[int(key)] = 1

def createFeatureMatrix():
	es = Elasticsearch()
	docmap = {}
	wordcount = -1

	for word in spamwords:
		print word.rstrip()
		wordcount = wordcount+1
		#doc = {\"fields\": [\"_id\"], \"query\": {\"bool\": {\"must\": [{\"match_phrase\":{\"text\": \"viagra\" }},{\"match\": {\"split\": \"train\"}}]}}}
		res = es.search(index="email_index",doc_type="document",body={"fields": ["_id"], "query": {"bool": {"must": [{"match_phrase":{"text": word }},{"match": {"split": "train"}}]}}})
		total = res['hits']['total']
		if total!=0:
			for hit in res['hits']['hits']:
				docid = hit['_id']
				tf = hit['_score']
				if docid in docmap:
					fmap = docmap[docid]
				else:
					fmap = {}
				fmap[wordcount]=float(tf)
				docmap[int(docid)]=fmap
	createTrainingFile(docmap,wordcount)

def createTrainingFile(docmap,wordcount):
	f = open('training_model_1','w')
	for i in trainingset:
		print i
		output = str(labelsf[i]) + " "
		if i in docmap:
			allwords = docmap[i]
			for word in range(0,wordcount):
				if word in allwords:
					output = output + str(word) + ":" + str(allwords[word]) + " "
				else:
					output = output + str(word) + ":0" + " "
		else:
			for word in range(0,wordcount):
				output = output + str(word) + ":" + "0" + " "
		f.write(output)
		f.write("\n")

def createTestFile(docmap,wordcount):
	f = open('test_model_1','w')
	for i in testset:
		print i
		output = str(labelsf[i]) + " "
		if i in docmap:
			allwords = docmap[i]
			for word in range(0,wordcount):
				if word in allwords:
					output = output + str(word) + ":" + str(allwords[word]) + " "
				else:
					output = output + str(word) + ":0" + " "
		else:
			for word in range(0,wordcount):
				output = output + str(word) + ":" + "0" + " "
		f.write(output)
		f.write("\n")

readLabels()
readTrainingIds()
readTestIds()
readSpamWords()
createFeatureMatrix()












