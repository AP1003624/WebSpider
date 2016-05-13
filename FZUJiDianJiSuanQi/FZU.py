# coding=utf8
# Create by 吴俊 on 2016/5/13

import urllib
import urllib2
import cookielib
import re

# 福州大学绩点运算
class FZU:

	def __init__(self):
		self.loginUrl = u''
		self.cookies = cookielib.CookieJar()
		self.postData = urllib.urlencode({

		})
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))

	def getPage(self):
		request = urllib2.Request(url = self.loginUrl, data=self.postData)
		result = urllib2.urlopen(request)
		# 打印登录内容
		print(result.read().decode(u'utf-8'))