# -*- coding:utf-8 -*-
from sklearn.svm import SVC
from sklearn import grid_search
import numpy as np
from sklearn import cross_validation as cs
from sklearn.externals import joblib
from picPreHandle import loadSplitedBinaryPixImg
import warnings

warnings.filterwarnings("ignore")

PKL = "captcha.pkl"

def load_data():
	dataset = np.loadtxt('train_data.txt',delimiter=',')
	return dataset

def cross_validation():
	dataset = load_data()
	row,col=dataset.shape
	X=dataset[:,:col-1]
	Y=dataset[:,-1]
	clf = SVC(kernel="linear",C=1)
	scores = cs.cross_val_score(clf,X,Y,cv=5)
	print("Accuracy:%0.2f (+/- %0.2f)" % (scores.mean(),scores.std()*2))

def train():
	dataset=load_data()
	row,col = dataset.shape
	X=dataset[:,:col-1]
	Y=dataset[:,-1]
	clf = SVC(kernel="linear",C=1)
	clf.fit(X,Y)
	joblib.dump(clf,PKL)


def searchBestParameter():
	parameters = {"kernel":("linear","poly","rbf","sigmoid"),"C":[1,100]}
	dataset=load_data()
	row,col=dataset.shape
	X=dataset[:,:col-1]
	Y=dataset[:,-1]
	svr = SVC()
	clf = grid_search.GridSearchCV(svr,parameters)
	clf.fit(X,Y)
	print clf.best_params_

def predict(pic_name):
	clf=joblib.load(PKL)
	rs=loadSplitedBinaryPixImg(pic_name)#get pixel data of splited image
	predictValue=[]
	for data in rs:
		predictValue.append(clf.predict(data)[0])
	predictValue = [str(int(i)) for i in predictValue]
	print "the captcha is :%s" %("".join(predictValue))
	return predictValue

if __name__=="__main__":
	# cross_validation()
	# searchBestParameter()
	# train()

	filePath = 'source/22.png'
	predict(filePath)