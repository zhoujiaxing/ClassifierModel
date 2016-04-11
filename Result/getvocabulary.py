import classifiermodel
import string
from pymongo import MongoClient
cates=["Auto","Business","Cricket","Entertainment/Bollywood","Health","Lifestyle","National","Politics","Sports","Technology","World"]
if __name__ == "__main__":
	model = classifiermodel.ClassifierModel()
	words = model.vectorizer.vocabulary_
	print "vecabulary number is %d ...."%len(words)
	file1 = open("vocabulary.txt","w")
	for word in words:
		file1.write(word.encode('utf8')+"\n")
	file1.close()

