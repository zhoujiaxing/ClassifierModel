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
		file1.write(word+"\n")
	file1.close()
	#test
	ret = {}
	for cate in cates:
		ret[cate] = 0
	ret["Other"] = 0
	dirc = model.dirctory
	for cate in cates:
		texts = dirc[cate][8000:9000]
		fileopen = open('./test5/'+cate[0:13]+".txt","w")
		fileopen.write(str(len(texts))+'\n')
		count = 0
		for text in texts:
			categorys = model.getCategorys(text)
			for category in categorys:
				ret[category] = ret[category] + 1
				fileopen.write(category+' ')
				if cate ==  category:
					count = count + 1
			fileopen.write("\n")
		fileopen.write(str(count))
		fileopen.write(str(float(count)/float(len(texts))*100)+'\%')
		fileopen.close()
		file1 = open("./test5/"+"ret.txt","w")
		file1.write(str(ret))
		file1.close()
		print "%s test is over...."%cate
