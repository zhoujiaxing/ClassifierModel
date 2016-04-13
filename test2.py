from classifier import Classifier
from pymongo import MongoClient
model = Classifier()

client = MongoClient('localhost',27017)
collection = client['mydb']['web']

cates = ["Auto","Business","Cricket","Entertainment/Bollywood","Health","Lifestyle","National","Politics","Sports","Technology","World"]

nc = {}
tnc = {}
for cate in cates:
	nc[cate] = tnc[cate] = 0
nc['Other'] = tnc['Other'] = 0

for cate in cates:
	fileopen = open('./Result/test7/'+cate[0:13]+'.txt','w')
	datas = collection.find({'category':cate})[8000:9000]
	count = 0
	for data in datas:
		text = data['article']
		category = model.getCategory(text)
		if category == cate:
			nc[cate] = nc[cate] + 1
		tnc[category] = tnc[category] + 1
		fileopen.write(category+'\n')
	fileopen.close()

fileopen = open('./Result/test7/result.txt','w')
fileopen.write('cate\t\trnum\t\ttnum\t\trecovery\tright\n')
for cate in cates:
	rnum = nc[cate]
	tnum = tnc[cate]
	recovery = rnum/1000.0
	right = rnum/(rnum+(tnum-rnum)/10.0)
	fileopen.write('%s\t\t%d\t\t%d\t\t%f\t%f\n'%(cate[0:4],rnum,tnum,recovery,right))
fileopen.write("Other\t\t%d"%tnc['Other'])

