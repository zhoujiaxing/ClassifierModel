from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from pymongo import MongoClient
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pymongo
import string
cates = ["Auto","Business","Cricket","Entertainment/Bollywood","Health","Lifestyle","National","Politics","Sports","Technology","World"]

class ClassifierModel(object):
	def __init__(self):
		self.dirctory = {}
		self.vectorizer = TfidfVectorizer(encoding='utf8',vocabulary=None,use_idf=True)
		self.classifiers = {}
		self.getDirctory()
		self.trainVectorizer(num=1000)
		self.trainClassifiers(num=650)
	def getDirctory(self):
		client = MongoClient('localhost',27017)
		collection = client["mydb"]["corpus"]
		datas = collection.find()
		#print len(datas)
		for data in datas:
			try:
				category = data['category']
				text = data['text']
				if self.dirctory.has_key(category):
					self.dirctory[category].append(text)
				else:
					self.dirctory.update({category:[text]})
			except:
				"No expect...."
		print "Dirctory Categoey number is %d..."%len(self.dirctory.keys())
	def trainVectorizer(self,num=1000):
		corpus = []
		for category in cates:
			corpus.extend(self.dirctory[category][0:num])
		self.vectorizer.fit_transform(corpus)
		print "train vector number is %d...."%len(corpus)
	def trainClassifiers(self,num=650):
		for category in cates:
			classifier = LogisticRegression(penalty='l2',C=1.0,tol=0.0001)
			train_x = []
			train_y = []
			for cate in cates:
				if cate == category:
					texts = self.dirctory[cate][0:num*10]
					for text in texts:
						train_x.append(self.getFeature(text))
						train_y.append(1)
				else:
					texts = self.dirctory[cate][0:num]
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
		deci_param["Cricket"] = 1
		deci_param["Lifestyle"] = 1
		deci_param["Business"] = 1
		deci_param["Auto"] = 1
		deci_param["National"] = 1
		deci_param["Entertainment/Bollywood"] = 1
		deci_param["Sports"] = 1
		deci_param["Health"] = 1
		deci_param["World"] = 1
		deci_param["Politics"] = 1
		deci_param["Technology"] = 1
		feature = self.getFeature(text)
		categorys = []
		for cate in cates:
			classifier = self.classifiers[cate]
			ans = classifier.decision_function(feature)[0]
			if ans > deci_param[cate]:
			#if ans > 0:
				categorys.append(cate)
		if categorys == []:
			return ['Other']
		return categorys
	'''
	def getCategory(self,text):
		category = None
		value  = 0
		feature = self.getFeature(text)
		for cate in cates:
			classifier = self.classifiers[cate]
			ans = classifier.decision_function(feature)[0]
			if cate == "Auto":
				category = cate
				value = ans
			if ans > value:
				category = cate
				value = ans
		return category
	'''
	def getCategory(self,text,thod = 1.0):
		feature = self.getFeature(text)
		for cate in cates:
			classifier = self.classifiers[cate]
			ans = classifier.decision_function(feature)[0]
			if ans > thod:
				return cate
		return 'Other'
def getVocabulary():
	vocabulary = {}
	file1 = open("vocabulary.txt","r")
	count = 0
	lines = file1.readlines()
	for line in lines:
		vocabulary.update({line.strip():count})
		count = count + 1
	file1.close()
	return vocabulary
