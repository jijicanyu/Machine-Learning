#!coding=utf-8

import jieba
import numpy
import random
import string
import re
from baidu import sql_search
from bs4 import BeautifulSoup
import urllib2

class tf_idf:

	def __init__(self):
		self.string=['，','。'," ","\n","\r","》","《","	","、"," ","："]
		self.num_all=100000000  ##百度语料库总数
		self.dict_ci_num={}   ##关键词在文章中出现的次数{"中国":100}
		self.dict_ci_tf={}    ##关键词在文章中的词频{"中国":0.012121}
		self.dict_ci_idf={}   ##关键词在语料库(此处为百度)中的idf值{"中国":0.01213}
		self.dict_ci_tfidf={} ##关键词tf_idf值{"中国":0.12112}


		self.get_content()    ## 获取待检测文章网页内容
		self.get_tf()		  ## 获取关键词tf值
		self.get_idf()		  ## 获取关键词idf值
		self.get_tf_idf()	  ## 获取关键词tf_idf值
		self.list_sort()      ## 按tf_idf大小排序

	def get_content(self):

		# with open("test.txt","r") as w:
		# 	content=w.read()

		content=urllib2.urlopen("http://news.qq.com/a/20150809/007091.htm?tu_biz=1.114.2.1").read()

		soup=BeautifulSoup(content,'lxml')                            #去除网页内html标签
		[script.extract() for script in soup.findAll('script')]    #把html里script，style给清理
		[style.extract() for style in soup.findAll('style')]
		reg1 = re.compile("<[^>]*>")                                #把所有的HTML标签全部清理
		content = reg1.sub('',soup.prettify())                       #格式化输出

		for i in string.punctuation:   ##去除字符串标点符号
			content=content.encode("utf-8").replace(i,'').decode("utf-8")

		for i in self.string+range(10):  ##去除特殊字符与数字
			content=content.encode("utf-8").replace(str(i),'').decode("utf-8")

		self.jieba_cut(content)

	def jieba_cut(self,content):
		a=jieba.cut(content)
		b="/".join(a)
		list_content=b.split("/")
		self.list_content_len=len(list_content)
		for i in list_content:
			if len(i)<16:                    ##剔除很长的单词
				num=(list_content.count(i))
				self.dict_ci_num[i]=num
			else:
				pass


	def get_tf(self):
		for key in self.dict_ci_num.keys():
			tf=float(self.dict_ci_num[key])/float(self.list_content_len)
			self.dict_ci_tf[key]=tf


	def get_idf(self):
		for key in self.dict_ci_num.keys():
			num=sql_search(key.encode("utf-8"))       ##通过百度搜索引擎查询idf
			idf=numpy.log(float(self.num_all)/float((num+1)))
			self.dict_ci_idf[key]=idf

	def get_tf_idf(self):
		for key in self.dict_ci_tf.keys():
			tf=self.dict_ci_tf[key]
			idf=self.dict_ci_idf[key]
			tf_idf=tf*idf
			self.dict_ci_tfidf[key]=tf_idf

	def list_sort(self):

		list_tfidf=sorted(self.dict_ci_tfidf.iteritems(), key=lambda d:d[1], reverse = True)

		for i in range(0,10):

			print list_tfidf[i][1],list_tfidf[i][0]

tf_idf()













