#!coding=utf-8

from dbOperation import dbOperation
import urllib2


def sql_search(keyword):
	cur=dbOperation()
	a=cur.queryWord(keyword)
	if len(a)>0:
		pass
	else:
		num=bing_api(keyword)
		dicts={
				"NAME":keyword,
				"NUM":num		
		}
		cur.Insert(dicts)

def bing_api(keyword):
	url=""
	req=urllib2.urlopen(url)
	return num