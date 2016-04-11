from classifiermodel import ClassifierModel
from sklearn.externals import joblib

cates = ["Auto","Business","Cricket","Entertainment/Bollywood","Health","Lifestyle","National","Politics","Sports","Technology","World"]

model = ClassifierModel()

joblib.dump(model.vectorizer,'./model/tfidfvectorizer.model')

for cate in cates:
	joblib.dump(model.classifiers[cate],'./model/'+cate[0:13]+'classifier.model')

