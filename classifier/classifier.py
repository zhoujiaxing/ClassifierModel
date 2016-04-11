from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from pymongo import MongoClient
from sklearn.externals import joblib

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#Determine the order of classification
cates = ['Cricket','Technology','Lifestyle','Auto','Politics','Health','Sports','Entertainment/Bollywood','Business','World','National']#0

'''
Provide two functions:
def getCategory(text)
	Get the only category for the text,otherwise get a 'Other'
def getCategorys()
	Get all possible categories for the text,otherwise get a ['other']
'''
class Classifier(object):
	def __init__(self):
		self.vectorizer = joblib.load('./model/tfidfvectorizer.model')
		self.classifier = {}
		for cate in cates:
			self.classifier[cate] = joblib.load('./model/'+cate[0:13]+'classifier.model')
	def getFeature(self,text):
		return self.vectorizer.transform([text]).toarray()[0]
	def getCategorys(self,text,thod=1):
		feature = self.getFeature(text)
		categorys = []
		for cate in cates:
			classifier = self.classifier[cate]
			ans = classifier.decision_function(feature)
			if ans > thod:
				categorys.append(cate)
		if categorys == []:
			categorys.append('Other')
		return categorys
	def getCategory(self,text,thod=1):
		feature = self.getFeature(text)
		for cate in cates:
			classifier = self.classifier[cate]
			ans = classifier.decision_function(feature)[0]
			if ans > thod:
				return cate
		return 'Other'
