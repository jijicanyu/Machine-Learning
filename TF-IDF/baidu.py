#!coding=utf-8

import urllib2
import re
from sql import sql_db

url_baidu="http://www.baidu.com/s?wd="
res=r"百度为您找到相关结果约(.*)个"
# keyword="博彩"

def baidu_search(keyword):
	try:
		url=url_baidu+keyword
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

def sql_search(keyword):
	cur=sql_db()
	a=cur.search_db(table='ci_num',name=keyword)
	if len(a)>0:            ##查询数据库,如果数据库中不存在，则利用百度搜索，并将结果保存到数据库。
		num=int(a[0][1])
		print "[Found...]keyword:%s,number:%s" % (keyword,str(num))   

		##########################更新数据库###########################
		# num=baidu_search(keyword)
		# cur.update_db(table='ci_num',name=keyword,num=num)
		# print "[Update...]keyword:%s,number:%s" % (keyword,str(num))
	else:
		num=baidu_search(keyword)
		print "[Spider...]keyword:%s,number:%s" % (keyword,str(num))
		try:
			cur.insert_db(table='ci_num',name=keyword,num=num)
			print "[Save...]{%s:%s}" % (keyword,str(num))
		except Exception,e:
			print e
	cur.close()
	return num


	


