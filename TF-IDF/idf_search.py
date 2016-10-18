#!coding=utf-8

import urllib2
import urllib
import re
import random
from ip_proxy import ip_proxy

url_baidu="http://www.baidu.com/s?wd="
res=r"百度为您找到相关结果约(.*)个"
url_bing="http://cn.bing.com/search?q="
res2=r"sb_count\"\>([^ ]*)"

with open("user-agents.txt",'r') as w:
	header_list=w.readlines()

list_ip_port=ip_proxy()

def baidu_search(keyword):
	try:
		url=url_baidu+urllib.quote(keyword)
		f=urllib2.urlopen(url)
		body=f.read()

		p=re.compile(res)
		L=p.findall(body)

		if len(L)>0:
			num=int(L[0].replace(",",""))
		else:
			num=99999999
	except Exception,e:
		print e
		num=99999999
	return num

def bing_search(keyword):
	try:
		url=url_bing+urllib.quote(keyword)
		header={'User-Agent':random.choice(header_list).replace("\n","").replace("\r",""),'Referer':'http://cn.bing.com/search'}
		ip_port=random.choice(list_ip_port).replace("\n","")
		# header={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36b'}
		print header
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

def sql_search(keyword,cur):
	a=cur.search_db(table='ci_num',name=keyword)
	if len(a)>0:            ##查询数据库,如果数据库中不存在，则利用百度搜索，并将结果保存到数据库。
		num=int(a[0][1])
		print "[Found...]keyword:%s,number:%s" % (keyword,str(num))   

		##########################更新数据库###########################
		# num=baidu_search(keyword)
		# cur.update_db(table='ci_num',name=keyword,num=num)
		# print "[Update...]keyword:%s,number:%s" % (keyword,str(num))
	else:
		# num=baidu_search(keyword)   ##百度
		num=bing_search(keyword)      ##必应
		print "[Spider...]keyword:%s,number:%s" % (keyword,str(num))
		try:
			cur.insert_db(table='ci_num',name=keyword,num=num)
			print "[Save...]{%s:%s}" % (keyword,str(num))
		except Exception,e:
			print e
	return num


num=bing_search("mima")



