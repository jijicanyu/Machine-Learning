#!coding=utf-8

import jieba
import numpy
import string
import re
from lib.bing_api import sql_search
from bs4 import BeautifulSoup
import urllib2
from lib.langconv import *

class tf_idf:

	res=ur"[\u4E00-\u9FA5]"

	def __init__(self,url):
		self.url=url
		self.string=['•','？','，','。'," ","\n","\r","》","《","	","、"," ","：",")","(","（","）","！",'【','】','“','”',"的"]
		self.num_all=2000000000  ##百度语料库总数
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
		try:
			# # with open(self.url,"r") as w:
			# 	content=w.read().lower()
			'''
			网页内容获取
			'''
			content=urllib2.urlopen(self.url, timeout=5).read().lower()
			soup=BeautifulSoup(content,'lxml')                            #去除网页内html标签
			try:
				content_title=soup.title.string
			except:
				content_title=""
			try:
				content_desc=soup.select("meta[name=\"description\"]")[0]['content']
			except:
				content_desc=""
			[script.extract() for script in soup.findAll('script')]    #把html里script，style给清理
			[style.extract() for style in soup.findAll('style')]
			reg1 = re.compile("<[^>]*>")                                #把所有的HTML标签全部清理
			content = reg1.sub('',soup.prettify())                       #格式化输出
			
			'''
			网页内容处理
			'''
			content=content_title*10+content_desc*10+content  ##增加标题与描述的权重
			
			content=Converter('zh-hans').convert(content)   ##繁体字转化为简体字

			p=re.compile(tf_idf.res)                        ##保留除中文字以外的字符
			L=p.findall(content)
			content_zw=""
			for i in L:
				content_zw=content_zw+i

			#print content_zw
			
		except Exception,e:
			print e
			
			return

		self.jieba_cut(content_zw)

	def jieba_cut(self,content):
		a=jieba.cut(content)
		b="/".join(a)
		list_content=b.split("/")

		self.list_content_len=len(list_content)
		for i in list_content:
			if 1<len(i)<12:                    ##剔除很长的单词
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
			num=sql_search(key)       ##通过百度搜索引擎查询idf
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
		num=len(list_tfidf)
		if num>20:
			nums=20
		else:
			nums=num
		for i in range(0,nums):
			try:
				print list_tfidf[i][1],list_tfidf[i][0]
			except Exception,e:
				print e
				pass


with open("./doc/url.txt","r") as w:
	f=[i.replace("\n","") for i in w.readlines()]

for i in f:
	tf_idf(i)
	break
	













