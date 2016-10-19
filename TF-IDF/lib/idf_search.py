#!coding=utf-8

import urllib2
import urllib
import jieba
import re
import random
from ip_proxy import ip_proxy
from dbOperation import dbOperation
import threading
import Queue
import time

url_baidu="http://www.baidu.com/s?wd="
res=r"百度为您找到相关结果约(.*)个"
url_bing="http://cn.bing.com/search?q="
url_sougou="https://www.sogou.com/web?query="
res2=r"sb_count\"\>([^ ]*)"
res3=r"scd_num\"\>([^<]*)"

with open("../doc/user-agents.txt",'r') as w:
	header_list=w.readlines()

def baidu_search(keyword):
	try:
		header={'User-Agent':random.choice(header_list).replace("\n","").replace("\r",""),'Referer':'http://www.sougou.com'}
		# ip_port=q_proxy.get()
		# print 'qsize_proxy',q_proxy.qsize()

		url=url_baidu+urllib.quote(keyword)
		req=urllib2.Request(url=url,headers=header)
		# req.set_proxy(ip_port,'http')
		f=urllib2.urlopen(req,timeout=2)
		body=f.read()
		# print body

		p=re.compile(res)
		L=p.findall(body)
		# print L

		if len(L)>0:
			num=int(L[0].replace(",",""))
			# q_proxy.put(ip_port)
			return num
		else:
			print 'error'
			q_keyword.put(keyword)
			return None
	except Exception,e:
		print e
		q_keyword.put(keyword)
		return None

def sougou_search(keyword):
	try:
		header={'User-Agent':random.choice(header_list).replace("\n","").replace("\r",""),'Referer':'http://www.sougou.com'}
		# ip_port=q_proxy.get()
		# print 'qsize_proxy',q_proxy.qsize()

		url=url_sougou+urllib.quote(keyword)
		req=urllib2.Request(url=url,headers=header)
		# req.set_proxy(ip_port,'http')
		f=urllib2.urlopen(req,timeout=2)
		body=f.read()
		# print body
 
		p=re.compile(res3)
		L=p.findall(body)
		# print L

		if len(L)>0:
			num=int(L[0].replace(",",""))
			# q_proxy.put(ip_port)
			return num
		else:
			print 'error'
			q_keyword.put(keyword)
			return None
	except Exception,e:
		print e
		q_keyword.put(keyword)
		return None


def bing_search(keyword):
	try:
		url=url_bing+urllib.quote(keyword)
		header={'User-Agent':random.choice(header_list).replace("\n","").replace("\r",""),'Referer':'http://cn.bing.com/search'}
		#ip_port=random.choice(list_ip_port).replace("\n","")
		# header={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36b'}
		# print header
		req=urllib2.Request(url=url,headers=header)
		# print ip_port
		# req.set_proxy(ip_port,'http')
		f=urllib2.urlopen(req,timeout=3)
		body=f.read()

		# print body

		p=re.compile(res2)
		L=p.findall(body)

		if len(L)>0:
			num=int(L[0].replace(",",""))
			print num
		else:
			bing_search(keyword)
	except Exception,e:
		print e
		bing_search(keyword)

def sql_search():
	while 1:
		print 'qsize_keyword',q_keyword.qsize()
		keyword=q_keyword.get()
		cur=dbOperation()
		a=cur.queryWord(keyword)   ##
		if len(a)>0:            ##查询数据库,如果数据库中不存在，则利用百度搜索，并将结果保存到数据库。
			num=int(a[0])
			print "[Found...]keyword:%s,number:%s" % (keyword.decode("utf-8"),str(num))   

			##########################更新数据库###########################
			# num=sougou_search(keyword)
			# cur.update_db(table='ci_num',name=keyword,num=num)
			# print "[Update...]keyword:%s,number:%s" % (keyword,str(num))
			pass
		else:
			num=baidu_search(keyword)   ##百度
			# num=bing_search(keyword)      ##必应
			# num=sougou_search(keyword)    ##搜狗
			time.sleep(0.5)
			if num!=None:
				dicts={
						'NAME':keyword,
						'NUM':num
				}
				print "[Spider...]keyword:%s,number:%s" % (keyword.decode("utf-8"),str(num))
				try:
					cur.Insert(dicts)
					print "[Save...]{%s:%s}" % (keyword.decode("utf-8"),str(num))
				except Exception,e:
					print e
	# return num

def jieba_cut(content):
	a=jieba.cut(content)
	b="/".join(a)
	list_content=list(set(b.split("/")))

	return list_content



with open("../doc/user-agents.txt",'r') as w:
	content=w.read()


list_content=jieba_cut(content)

print "list_content_num",len(list_content)

q_keyword=Queue.Queue()
q_proxy=Queue.Queue()

for i in list_content:
	q_keyword.put(i)

sql_search()