#!coding=utf-8
'''
获取http代理
'''

import urllib2

def ip_proxy():
	url="http://api.goubanjia.com/api/get.shtml?order=154524b1a3dd141437e18444d691bc74&num=4000&carrier=0&protocol=1&an1=1&sp1=1&sp2=2&sp3=3&sort=1&system=1&distinct=0&rettype=1&seprator=%0A"
	# url="http://www.baidu.com"
	req=urllib2.urlopen(url)
	ip_list=[i.replace("\r","").replace("\n","") for i in req.readlines()]
	return ip_list


# ip_proxy()
