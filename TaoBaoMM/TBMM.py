# coding=utf8
# Create by 吴俊 on 2016/5/13

import urllib
import urllib2
import re
import os
from Tool import *

# 抓取MM
class TBMMSpider:

	# 页面初始化
	def __init__(self):
		self.siteUrl = u'http://mm.taobao.com/json/request_top_list.htm'
		self.tool = Tool()
		self.user_agent = u'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		# 初始化headers
		self.headers = {u'User-Agent': self.user_agent}

	# 获取索引页面的内容
	def getPage(self,pageIndex):
		url = self.siteUrl+u'?page='+str(pageIndex)
		print(url)
		request = urllib2.Request(url,headers = self.headers)
		response = urllib2.urlopen(request)
		return response.read().decode(u'gbk')

	# 获取索引页面所有MM的信息，list格式
	def getContents(self,pageIndex):
		page = self.getPage(pageIndex)
		patter = re.compile(u'<div class="list-item.*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)" .*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
		items = re.findall(patter,page)
		contents = []
		for item in items:
			# item[0]是MM详情页，item[1]是MM头像地址，item[2]是MM姓名，item[3]是MM年龄，item[4]是MM居住地
			# print u'http:'+item[0],u'http:'+item[1],item[2],item[3],item[4]
			contents.append([u'http:'+item[0],u'http:'+item[1],item[2],item[3],item[4]])
		return contents

	# 获取MM个人详情页面
	def getDetailPage(self,infoUrl):
		request = urllib2.Request(infoUrl,headers=self.headers)
		response = urllib2.urlopen(request)
		return response.read().decode(u'gbk')

	# 获取个人文字简介
	def getBrief(self,page):
		patter = re.compile(u'<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
		result = re.search(patter,page)
		if result:
			return self.tool.replaceHTMLTag(result.group(1))
		else:
			return None

	# 获取页面所有图片
	def getAllImg(self,page):
		patter = re.compile(u'<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
		# 个人信息页面所有代码
		content = re.search(patter,page)
		# 从代码中提取图片
		patterImg = re.compile(u'<img.*?src="(.*?)".*?>',re.S)
		print(content)
		if content:
			images = re.findall(patterImg,content.group(1))
			return images
		else:
			return None

	# 保存多张写真图片
	def saveImgs(self,images,name):
		number = 1
		print(u'发现'+name+u'共有'+len(images)+u'张照片')
		for imageUrl in images:
			splitPath = imageUrl.split(u'.')
			fTail = splitPath.pop()
			if len(fTail)>3:
				fTail = 'jpg'
			fileName = name+u'/'+str(number)+u'.'+fTail
			self.saveImg(imageUrl,fileName)
			number+=1

	# 保存头像
	def saveIcon(self,iconURL,name):
		splitPath = iconURL.split(u'.')
		fTail = splitPath.pop()
		fileName = name+u'/icon.'+fTail
		self.saveImg(iconURL,fileName)

	# 写入图片【传入图片地址，文件名，保存单张图片】
	def saveImg(self,imgUrl,fileName):
		u = urllib.urlopen(imgUrl)
		data = u.read()
		f = open(fileName,u'wb')
		f.write(data)
		f.flush()
		f.close()

	# 写入文本
	def saveBrief(self,content,name):
		fileName = name+u'/'+name+u'.txt'
		f = open(fileName,u'w+')
		print(u'正在偷偷保存她的个人信息为'+fileName)
		f.write(content.encode('utf-8'))
		f.flush()
		f.close()

	# 创建新目录
	def mkdir(self,path):
		path = path.strip()
		# 判断路径是否存在，存在为True，不存在为False
		isExist = os.path.exists(path)
		# 判断结果
		if not isExist:
			# 如果不存在则创建目录
			# 创建目录操作函数
			os.makedirs(path)
			return True
		else:
			# 如果目录存在则不创建，并提示目录已存在
			return False

	def savePageInfo(self,pageIndex):
		contents = self.getContents(pageIndex)
		for item in contents:
			print u'发现一位模特，名字叫',item[2],u'，芳龄',item[3],u'，她在',item[4]
			print u'正在偷偷地保存',item[2],u'的信息'
			print u'又意外地发现她的个人地址是',item[0]
			# 个人详情页面的URL
			detailURL = item[0]
			print(detailURL)
			# 得到个人详情页面代码
			detailPage = self.getDetailPage(detailURL)
			# 获取个人简介
			brief = self.getBrief(detailPage)
			self.mkdir(item[2])
			# 判断个人简介是否为空
			if brief:
				print(brief)
				# 保存个人简介
				self.saveBrief(brief,item[2])
				# 获取所有图片列表
				images = self.getAllImg(detailPage)
				print(len(images))
				# 保存图片
				self.saveImgs(images,item[2])
			# 保存头像
			self.saveIcon(item[1],item[2])

	def savePagesInfo(self,start,end):
		for i in range(start,end+1):
			print u'正在偷偷寻找第',i,u'个地方，看看MM们在不在'
			self.savePageInfo(i)

if __name__ == u'__main__':
	# 传入起止页面即可，在此传入了2,10，表示抓取第2到10页的MM
	spider = TBMMSpider()
	spider.savePagesInfo(1,10)