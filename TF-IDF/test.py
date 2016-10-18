#!coding=utf-8

from langconv import *

line="澳门"
line=Converter('zh-hant').convert(line)
print(line)
