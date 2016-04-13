from classifiermodel import ClassifierModel
from pymongo import MongoClient


cates=["Auto","Business","Cricket","Entertainment/Bollywood","Health","Lifestyle","National","Politics","Sports","Technology","World"]

model = ClassifierModel()
def getTrainData():
	client = MongoClient('localhost',27017)
	collection = cilent['mydb']['corpus']
	corpus = {}
	for cate in cates:
		corpus[cate] = []
		datas = collection.find({'category':cate})
		for data in datas:
			text = data['text']
			corpus[cate].append(text)

def getTestData():
	client = MongoClient('localhost',27017)
	collection = client['mydb']['corpus']
	corpus = {}

if __name__ == "__main__":
	client = MongoClient('localhost',27017)
	collection = client['mydb']['corpus']
	dirctory = model.dirctory
	testdata = {}
	nc = {}
	tnc = {}
	for cate in cates:
		nc[cate] = 0
		tnc[cate] = 0
		testdata[cate] = dirctory[cate][6500:7500]
	nc['Other'] = tnc['Other'] = 0
	for cate in cates:
		texts = testdata[cate]
		for text in texts:
			categorys = model.getCategorys(text)
			for category in categorys:
				if cate == category:
					nc[category] = nc[category] + 1
				tnc[category] = tnc[category] + 1
	fileopen = open("Testresult4.txt",'w')
	fileopen.write("1\n")
	fileopen.write('cate\t\trecovery\ttotal\trecovery\tright\n')
	for cate in cates:
		right = float(nc[cate])/float(float(tnc[cate]-nc[cate])/10.0+nc[cate])*100
		recovery = float(nc[cate])/1000.0*100
		fileopen.write("%s\t\t%d\t\t\t%d\t%f\t%f\n"%(cate[0:4],nc[cate],tnc[cate],recovery,right))
	fileopen.write("%s\t%d\n"%('Other',tnc['Other']))
	fileopen.close()
