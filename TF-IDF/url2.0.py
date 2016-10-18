
#coding=utf-8
import urllib2
import urllib
import sys
import re
import time
# import xlwt
# import urlparse

question_word=raw_input(unicode('百度一下:','utf-8').encode('utf-8'))
num=int(raw_input(unicode('抓取页数:','utf-8').encode('utf-8')))
num=num*1
x=0
y=0
name=[]
urls=[]
title=str(question_word)

def search(question_word,x,urls,name):
	url = "http://www.baidu.com/s?wd=" + urllib.quote(question_word.decode(sys.stdin.encoding).encode('gbk'))+'&pn='+str(x)
	htmlbody=urllib2.urlopen(url).read()

	res=r'data-tools=\'\{\"title\":\"(.*)\",\"url\":\"(.*)\"\}\'>'
	p_tel=re.compile(res)
	htmllist=p_tel.findall(htmlbody)
	for i in htmllist:
		name.append(i[0])
		urls.append(i[1])
	x+=1
	time.sleep(2)
	if x>num:
		pass
	else:
		search(question_word,x,urls,name)

try:
	print u'正在启动爬虫.....请稍等.....'
	search(question_word,x,urls,name)
	# workbook=xlwt.Workbook()
	# sheet1=workbook.add_sheet('sheet1',cell_overwrite_ok=True)
	# for i in range(len(name)):
	# 	sheet1.write(i,0,name[i].decode('utf-8'))
	print ''
	pradaddaaint u'启动完毕...开始爬取......'
	f1=open('url.txt','w')
	for i in range(len(urls)):
		try:
			y+=1
			f=urllib2.urlopen(urls[i],timeout=3)
			url_true=f.geturl()

			# f=urlparse.urlparse(url_true)
			# url_host="http://"+f.netloc
			# print '('+str(y)+')'+str(url_host)
			# sheet1.write(i,1,url_host)

			# print '('+str(y)+')'+str(url_true)
			# sheet1.write(i,1,url_true)
			print url_true
			f1.write(url_true+'\n')
		except Exception,e:
			pass
	f1.close()		
	# workbook.save('test.xls')
	print u'爬取完毕'
except:
	pass


