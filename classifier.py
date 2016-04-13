from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from pymongo import MongoClient
from sklearn.externals import joblib

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

CATE_OTHERS = 'Others'
CATE_SPORTS = 'Sports'
CATE_CRICKET = 'Cricket'
CATE_ENTERTAIMENT = 'Entertainment/Bollywood'
CATE_AUTO = 'Auto'
CATE_TECHNOLOGY = 'Technology'
CATE_LIFESTYLE = 'Lifestyle'
CATE_HEALTH = 'Health'
CATE_BUSINESS = 'Business'
CATE_WORLD = 'World'
CATE_POLITICS = 'Politics'
CATE_EDUCATION = 'Education'
CATE_NATIONAL = 'National'

cate_threshold_hindi = {
	CATE_SPORTS: 0.8,
	CATE_CRICKET: 0.9,
	CATE_ENTERTAIMENT: 0.9,
	CATE_AUTO: 1,
	CATE_TECHNOLOGY: 1.1,
	CATE_LIFESTYLE: 1,
	CATE_HEALTH: 1,
	CATE_BUSINESS: 0.5,
	CATE_WORLD: 1.4,
	CATE_POLITICS: 1.9,
	CATE_EDUCATION: 1,
	CATE_NATIONAL: 0.5,
}

cates = ['Cricket','Technology','Lifestyle','Auto','Politics','Health','Sports','Entertainment/Bollywood','Business','World','National']#0


class Classifier(object):
	def __init__(self):
		self.vectorizer = joblib.load('./model/tfidfvectorizer.model')
		self.classifier = {}
		for cate in cates:
			self.classifier[cate] = joblib.load('./model/'+cate[0:13]+'classifier.model')
	def getFeature(self,text):
		feature = self.vectorizer.transform([text]).toarray()[0].reshape(1, -1)
		return feature
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
		try:
			for cate in cates:
				classifier = self.classifier[cate]
				ans = classifier.decision_function(feature)[0]
				if ans > cate_threshold_hindi[cate]:
					return cate
			return 'Other'
		except:
			"nothing"
