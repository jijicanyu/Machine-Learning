#!coding=utf-8

import urllib2
import urllib
import re

url_baidu="http://www.baidu.com/s?wd="
res=r"百度为您找到相关结果约(.*)个"
url_bing="http://cn.bing.com/search?q="
res2=r"sb_count\"\>([^ ]*)"

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
		f=urllib2.urlopen(url)
		body=f.read()

		p=re.compile(res2)
		L=p.findall(body)

		if len(L)>0:
			num=int(L[0].replace(",",""))
		else:
			num=99999999
	except Exception,e:
		print e
		num=99999999
	return num

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


# print bing_search("的")
	


