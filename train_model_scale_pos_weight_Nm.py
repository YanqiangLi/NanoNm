import sys,os,re
import gzip
import numpy as np
from sklearn import svm
from sklearn import datasets
from sklearn.model_selection import train_test_split as ts
import matplotlib
import joblib
import pickle
matplotlib.use('Agg')
from matplotlib import pyplot
from matplotlib import pyplot as plt
from collections import defaultdict
from xgboost import plot_importance
from collections import Counter
import matplotlib.pyplot as plt

#######
#tpp="mRNA"
tpp=sys.argv[1]
X,Y=[],[]
######################
for i in open("./%s.mod.tsv"%(tpp),"r"):
    ele=i.rstrip().split()
    # ~ GXB01170_2018.fast5|233|23,3,1,00,2,3	0	0|0|0|0|0	0.47062142444662086|0.8176029853529686|0.7531814474848483|-0.0835983106934529|-0.5416802793696001	0.14888963355157137|0.1977707177676313|0.11147011292496822|0.18032028688587404|0.15884083915957087	0.5053374754088856|0.9240774715516673|0.7871817035819118|-0.06103521168167164|-0.5495652071815835   15|6|6|138|64
    insert=[]
    for item in [ele[3],ele[4],ele[5],ele[6]]:
        for itemsub in item.split("|"):
        	insert.append(float(itemsub))
    X.append(insert)
    Y.append(1)
#####################
for i in open("./%s.unmod.tsv"%(tpp),"r"):
    ele=i.rstrip().split()
    # ~ GXB01170_2018.fast5|233|23,3,1,00,2,3	0	0|0|0|0|0	0.47062142444662086|0.8176029853529686|0.7531814474848483|-0.0835983106934529|-0.5416802793696001	0.14888963355157137|0.1977707177676313|0.11147011292496822|0.18032028688587404|0.15884083915957087	0.5053374754088856|0.9240774715516673|0.7871817035819118|-0.06103521168167164|-0.5495652071815835   15|6|6|138|64
    insert=[]
    for item in [ele[3],ele[4],ele[5],ele[6]]:
        for itemsub in item.split("|"):
        	insert.append(float(itemsub))
    X.append(insert)
    Y.append(0)
#######################################
scale_pos_weight1= Y.count(1)/Y.count(0)


X=np.array(X)
Y=np.array(Y)
#########################################
#split the data to  4:1
x_train,x_test,y_train,y_test = ts(X,Y,test_size=0.2,random_state=0, shuffle=True)
################################################################################################
######################################################################################################################################################################################
from xgboost.sklearn import XGBClassifier
from sklearn import metrics
print(Counter(Y))
print(Counter(y_train))
print(Counter(y_test))
#clf = XGBClassifier(n_jobs=-1,learning_rate=0.3,tree_method='gpu_exact',n_estimatores=58,alpha=0.1,gamma=0,reg_lambda=10,in_child_weight=1,max_depth=20,colsample_bytree=0.8,subsample=1,objective="binary:logistic")
print(scale_pos_weight1)
clf = XGBClassifier(n_jobs=-1,learning_rate=0.3,n_estimatores=158,alpha=0.1,gamma=0,scale_pos_weight=scale_pos_weight1,reg_lambda=10,in_child_weight=1,max_depth=20,colsample_bytree=0.8,subsample=1,objective="binary:logistic")
clf.fit(x_train, y_train)

y_pred = clf.predict(x_test)
### model evaluate
accuracy = metrics.accuracy_score(y_test,y_pred)
tr_auc = metrics.roc_auc_score(y_test,y_pred)
#########
print(tpp,"accuracy:\t",accuracy,"auc:\t",tr_auc)

###########################################################################################
y_pred_proba = clf.predict_proba(x_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)
print(tpp,"new_accuracy:\t",accuracy,"new_auc:\t",auc)
plt.figure()
plt.rcParams["figure.figsize"] = (10,10)
plt.plot(fpr,tpr,label="%s_mRNA, auc=%0.2f)" %(tpp,auc))
plt.plot([0, 1], [0, 1], color='black', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')

plt.legend(loc=4)
plt.savefig('%s.new_Nm.auc.pdf'%(tpp))
plt.close("all")

filename = '%s.m'%(tpp)
pickle.dump(clf, open(filename, 'wb'))
