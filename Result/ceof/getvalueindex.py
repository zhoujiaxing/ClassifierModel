import classifiermodel
import string
from pymongo import MongoClient
cates=["Auto","Business","Cricket","Entertainment/Bollywood","Health","Lifestyle","National","Politics","Sports","Technology","World"]
def getIndex(threshold=0.001):
	index = []
	for cate in cates:
		file1 = open("C_"+cate[0:13]+".txt","r")
		lines = file1.readlines()
		count = 0
		for line in lines:
			value = float(line.strip())
			if value > threshold or value < -threshold:
				index.append(count)
			count = count + 1
	print len(set(index))
	print "getindex is over...."
def getFeature(index):
	feature = []
	dic = {}
	file1 = open("voca.txt","r")
	lines = file1.readlines()
	count = 0
	for line in lines:
		feat = line.strip()
		dic.update({count:feat})
		count = count + 1
	for i in index:
		feature.append(dic[i])
	file1.close()
	file1 = open("tmp.txt","w")
	for feat in feature:
		file1.write(feat+"\n")
	file1.close()
	print "getfeature is over...."
if __name__ == "__main__":
	model = classifiermodel.ClassifierModel()
	for cate in cates:
		file1 = open("./ceof1/"+"C_"+cate[0:13]+".txt","w")
		array = model.classifiers[cate].coef_[0]
		for a in array:
			file1.write(str(a)+'\n')
		file1.close()
		
