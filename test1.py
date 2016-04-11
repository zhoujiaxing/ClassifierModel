from classifiermodel import ClassifierModel
from pymongo import MongoClient

cates = ["Auto","Business","Cricket","Entertainment/Bollywood","Health","Lifestyle","National","Politics","Sports","Technology","World"]

client = MongoClient('localhost',27017)

collection = client['mydb']['corpus']

model = ClassifierModel()

for cate in cates:
	fileopen = open('./Result/test5/'+cate[0:13]+'.txt','w')
	datas = collection.find({'category':cate})[6500:7500]
	count = 0
	for data in datas:
		text = data['text']
		category = model.getCategory(text)
		if category == cate:
			count = count + 1
		fileopen.write(category+'\n')
	fileopen.write(str(count)+'\n')
	fileopen.close()
