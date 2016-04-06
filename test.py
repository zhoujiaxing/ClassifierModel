import classifiermodel
import string
from pymongo import MongoClient
cates=["Auto","Business","Cricket","Entertainment/Bollywood","Health","Lifestyle","National","Politics","Sports","Technology","World"]
if __name__ == "__main__":
	model = classifiermodel.ClassifierModel()
	words = model.vectorizer.get_feature_names()
	print "vecabulary number is %d ...."%len(words)
	file1 = open("vecabulary.txt","w")
	for word in words:
		file1.write(word.encode('utf8')+"\n")
	file1.close()
	#test
	dirc = model.dirctory
	for cate in cates:
		texts = dirc[cate][5000:6000]
		fileopen = open(cate[0:13]+".txt","w")
		fileopen.write(str(len(texts))+'\n')
		count = 0
		for text in texts:
			categorys = model.getCategorys(text)
			for category in categorys:
				fileopen.write(category+' ')
				if cate ==  category:
					count = count + 1
			fileopen.write("\n")
		fileopen.write(str(count))
		fileopen.write(str(float(count)/float(len(texts))*100)+'\%')
		fileopen.close()
		print "%s test is over...."%cate
