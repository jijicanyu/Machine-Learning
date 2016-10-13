#!coidng=utf-8

import jieba
import numpy
import random


with open("test.txt","r") as w:
	f=w.read().replace("\n","").replace(" ","")

a=jieba.cut(f)
b="/".join(a)
list_1=b.split("/")
############################################

dict_ci_num={}
dict_ci_tf={}

for i in list_1:
	nums=(list_1.count(i))
	dict_ci_num[i]=nums

############################################

len_sum=len(list_1)
for key in dict_ci_num.keys():
	value=dict_ci_num[key]
	tf=float(value)/float(len_sum)
	dict_ci_tf[key]=tf

# print(dict_ci_tf)

############################################
sums=10000
dict_ci_allnum={}
dict_ci_idf={}

for key in dict_ci_num.keys():
	a=random.randint(100,5000)   ###google search
	dict_ci_allnum[key]=a

# print dict_ci_allnum

for key in dict_ci_allnum.keys():
	num_key=dict_ci_allnum[key]
	idf=numpy.log(sums/(num_key+1))
	dict_ci_idf[key]=idf

#print dict_ci_idf


###############################
dict_ci_tfidf={}

for key in dict_ci_tf.keys():
	tf=dict_ci_tf[key]
	idf=dict_ci_idf[key]

	tf_idf=tf*idf

	dict_ci_tfidf[key]=tf_idf


#print dict_ci_tfidf


list_tfidf=sorted(dict_ci_tfidf.iteritems(), key=lambda d:d[1], reverse = True)

for i in list_tfidf:
	print i[1],i[0]















