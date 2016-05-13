# coding=utf8
# Create by 吴俊 on 2016/5/12

import urllib
import urllib2
import re
from Tool import *


# 参考链接：http://tieba.baidu.com/p/3138733512?see_lz=1&pn=1
# 百度贴吧爬虫类
class BDTB:
	# 初始化，传入基地址，是否只看楼主的参数，是否写入楼层信息
	def __init__(self, baseUrl, seeLZ=1, floorTag=1):
		'''
		http://  代表资源传输使用http协议
		tieba.baidu.com 是百度的二级域名，指向百度贴吧的服务器。
		/p/3138733512 是服务器某个资源，即这个帖子的地址定位符
		see_lz和pn是该URL的两个参数，分别代表了只看楼主和帖子页码，等于1表示该条件为真】
		:param baseUrl: 个帖子的地址定位符,如http://tieba.baidu.com/p/3138733512
		:param seeLZ: 是否只看楼主的参数,1表示该条件为真
		:return:
		'''
		# base链接地址
		self.baseUrl = baseUrl
		# 是否只看楼主，默认为1【1：看，0：不看】
		self.seeLZ = u'?see_lz=' + str(seeLZ)
		# HTML标签剔除工具类对象
		self.tool = Tool()
		# 全局file变量，文件写入操作对象
		self.file = None
		# 楼层标号，初始为1
		self.floor = 1
		# 默认标题，如果没有成功获取到标题的话则会用这个标题
		self.defaultTitle = u'百度贴吧'
		# 是否写入楼层信息标记，默认是1【1：写入，0：不写入】
		self.floorTag = floorTag

	# 传入页码，获取该页帖子的代码
	def getPage(self, pageNum):
		try:
			# 构建URL
			url = self.baseUrl + self.seeLZ + '&pn=' + str(pageNum)
			# print(url)
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			# print(response.read())
			# 返回utf-8格式编码内容
			return response.read().decode(u'utf-8')
		# 无法连接，报错
		except urllib2.URLError, e:
			if hasattr(e, u'reason'):
				print(u'连接百度贴吧失败，错误原因：', e.reason)
				return None

	# 获取帖子标题
	def getTitle(self, page):
		# 得道帖子标题的正则表达式
		patter = re.compile(u'<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
		result = re.search(patter, page)
		if result:
			# print(result.group(1).strip())
			# 如果存在，则返回标题
			return result.group(1).strip()
		else:
			return None

	# 获取帖子一共有多少页
	def getPageNum(self, page):
		# 获取帖子页数的正则表达式
		patter = re.compile(u'<li class="l_reply_num.*?</span>.*?>(.*?)</span>', re.S)
		result = re.search(patter, page)
		if result:
			# print(result.group(1).strip())
			return result.group(1).strip()
		else:
			return None

	# 获取每一层楼的内容，传入页面内容
	def getContent(self, page):
		# 匹配所有楼层的内容
		patter = re.compile(u'<div id="post_content_.*?>(.*?)</div>', re.S)
		items = re.findall(patter, page)
		contents = []
		for item in items:
			content = u'\n' + self.tool.replaceHTMLTag(item) + u'\n'
			contents.append(content.encode(u'utf-8'))
		return contents

	def setFileTitle(self, title):
		# 如果标题不是为None，即成功获取到标题
		if title is not None:
			self.file = open(title + u'.txt', u'w')
		else:
			self.file = open(self.defaultTitle + u'.txt', u'w+')

	def writeData(self, contents):
		# 向文件写入每一楼的信息
		for item in contents:
			if self.floorTag == '1':
				# 楼之间的分隔符
				floorLine = u'\n' + u'===============================' + str(self.floor) + u'==============================='
				print(floorLine)
				self.file.write(floorLine)
			self.file.write(item)
			self.floor += 1

	def start(self):
		indexPage = self.getPage(1)
		pageNum = self.getPageNum(indexPage)
		title = self.getTitle(indexPage)
		self.setFileTitle(title)
		if pageNum == None:
			print(u'URL已失效，请重试......')
			return
		try:
			print(u'该帖子共有' + str(pageNum) + u'页')
			for i in range(1, int(pageNum) + 1):
				print(u'正在写入第' + str(i) + u'页数据')
				page = self.getPage(i)
				contents = self.getContent(page)
				self.writeData(contents)
		# 出现异常写入
		except Exception, e:
			print(u'写入异常，原因：' + e.message)
		finally:
			# 写完关闭文件
			self.file.flush()
			self.file.close()
			print(u'写入任务完成!!!')


if __name__ == '__main__':
	print(u'请输入帖子代号')
	baseURL = u'http://tieba.baidu.com/p/'+str(raw_input(u'http://tieba.baidu.com/p/'))
	seeLZ = raw_input(u'是否只获取楼主发言，是输入1，否输入0\n')
	floorTag = raw_input(u'是否写入楼层信息，是输入1，否输入0\n')
	bdtbSpider = BDTB(baseURL, seeLZ, floorTag)
	bdtbSpider.start()
