from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from pymongo import MongoClient
import pymongo
import string
cates = ["Auto","Business","Cricket","Entertainment/Bollywood","Health","Lifestyle","National","Politics","Sports","Technology","World"]


class ClassifierModel(object):
	def __init__(self):
		self.dirctory = {}
		self.vectorizer = TfidfVectorizer(vocabulary=getVocabulary())
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
				"No expect....i"
		print "Dirctory Categoey number is %d..."%len(self.dirctory.keys())
	def trainVectorizer(self):
		corpus = []
		for category in cates:
			corpus.extend(self.dirctory[category])
		self.vectorizer.fit_transform(corpus)
		print "train vector number is %d...."%len(corpus)
	def trainClassifiers(self):
		number = 1000
		for category in cates:
			classifier = LogisticRegression()
			train_x = []
			train_y = []
			for cate in cates:
				if cate == category:
					texts = self.dirctory[cate][5000:5000+number*10]
					for text in texts:
						train_x.append(self.getFeature(text))
						train_y.append(1)
				else:
					texts = self.dirctory[cate][5000:5000+number]
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
		deci_param = {}
		deci_param["Cricket"] = 0.7
		deci_param["Lifestyle"] = 0.7
		deci_param["Business"] = 0.7
		deci_param["Auto"] = 0.7
		deci_param["National"] = 0.7
		deci_param["Entertainment/Bollywood"] = 0.7
		deci_param["Sports"] = 0.7
		deci_param["Health"] = 0.7
		deci_param["World"] = 0.7
		deci_param["Politics"] = 0.7
		deci_param["Technology"] = 0.7

		feature = self.getFeature(text)
		categorys = []
		for cate in cates:
			classifier = self.classifiers[cate]
			ans = classifier.decision_function(feature)[0]
			if ans > deci_param[cate]:
				categorys.append(cate)
		if categorys == []:
			return ['Other']
		return categorys
def getVocabulary():
	vocabulary = {}
	file1 = open("tmp.txt","r")
	count = 0
	lines = file1.readlines()
	for line in lines:
		vocabulary.update({line.strip():count})
		count = count + 1
	file1.close()
	return vocabulary
