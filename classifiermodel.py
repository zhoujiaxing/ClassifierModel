from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from pymongo import MongoClient
import pymongo
import string
cates = ["Auto","Business","Cricket","Entertainment/Bollywood","Health","Lifestyle","National","Politics","Sports","Technology","World"]


class ClassifierModel(object):
	def __init__(self):
		self.dirctory = {}
		self.vectorizer = TfidfVectorizer()
		self.classifiers = {}
		self.getDirctory()
		self.trainVectorizer()
		self.trainClassifiers()
	def getDirctory(self):
		client = MongoClient('localhost',27017)
		collection = client["mydb"]["web"]
		datas = collection.find()
		#print len(datas)
		for data in datas:
			try:
				category = data['category']
				text = data['article']
				if self.dirctory.has_key(category):
					self.dirctory[category].append(text)
				else:
					self.dirctory.update({category:[text]})
			except:
				"No expect...."
		print "Dirctory Categoey number is %d..."%len(self.dirctory.keys())
	def trainVectorizer(self):
		corpus = []
		for category in cates:
			corpus.extend(self.dirctory[category][0:5000])
		self.vectorizer.fit_transform(corpus)
		print "train vector number is %d...."%len(corpus)
	def trainClassifiers(self):
		number = 300
		for category in cates:
			classifier = LogisticRegression()
			train_x = []
			train_y = []
			for cate in cates:
				if cate == category:
					texts = self.dirctory[cate][0:number*10]
					for text in texts:
						train_x.append(self.getFeature(text))
						train_y.append(1)
				else:
					texts = self.dirctory[cate][0:number]
					for text in texts:
						train_x.append(self.getFeature(text))
						train_y.append(0)
			classifier.fit(train_x,train_y)
			self.classifiers.update({category:classifier})
			print "%s classifier train is over...."%category
		print "All classifier train is over...."
	def getFeature(self,text):
		return self.vectorizer.transform([text]).toarray()[0]
	def getCategorys(self,text):
		feature = self.getFeature(text)
		categorys = []
		for cate in cates:
			classifier = self.classifiers[cate]
			ans = classifier.predict(feature)[0]
			if ans == 1:
				categorys.append(cate)
		if categorys == []:
			return ['Other']
		return categorys
