import classifiermodel
import string
from pymongo import MongoClient
cates=["Auto","Business","Cricket","Entertainment/Bollywood","Health","Lifestyle","National","Politics","Sports","Technology","World"]
if __name__ == "__main__":
	client = MongoClient("127.0.0.1",27017)
	db = client["mydb"]["corpus1"]
	model = classifiermodel.ClassifierModel()
	ret = {}
	for cate in cates:
		ret[cate] = 0
	ret["Other"] = 0
	dirc = model.dirctory
	for cate in cates:
		texts = dirc[cate]
		for text in texts:
			categorys = model.getCategorys(text)
			if len(categorys) == 1 and categorys[0] == cate:
				db.insert({'category':cate,'text':text})
				ret[categorys[0]] = ret[categorys[0]] + 1
		print "%s insert is over...."%cate
		file1 = open("./test3/"+"ret.txt","w")
		file1.write(str(ret))
		file1.close()
		print "%s test is over...."%cate
