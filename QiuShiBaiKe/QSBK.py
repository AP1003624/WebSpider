# coding=utf8
# Create by 吴俊 on 2016/5/10

import urllib
import urllib2
import re
import thread
import time

# 糗事百科爬虫类
class QSBK:

	# 初始化方法，定义一些变量
	def __init__(self):
		self.pageIndex = 1
		self.user_agent = u'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		# 初始化headers
		self.headers = {u'User-Agent': self.user_agent}
		# 存放段子的变量，每一个元素是每一页的段子们
		self.stories = []
		# 存放程序是否继续运行的变量
		self.enable = False

	# 传入某一页的索引获得页面代码
	def getPage(self, pageIndex):
		try:
			url = u'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
			# 构建请求的request
			request = urllib2.Request(url, headers = self.headers)
			# 利用urlopen获取页面代码
			response = urllib2.urlopen(request)
			# 将页面转化为utf-8编码
			pageCode = response.read().decode(u'utf-8')
			return pageCode
		except urllib2.URLError, e:
			if hasattr(e, u'reason'):
				print(u'连接糗事百科失败，错误原因：', e.reason)
				return None

	# 根据每个story用正则表达式提取详细信息
	def getStoryDetail(self,story):
		# print(story)
		# 已过滤掉含图片部分，只提取文字
		authour = re.findall('<h2>(.*?)</h2>',story,re.S)[0].strip()
		contxt = re.findall('<div class="content">(.*?)</div>',story,re.S)[0].replace("<br/>","\n").strip()
		good = re.findall('<span class="stats-vote.*?class="number">(.*?)</i>',story,re.S)[0].strip()
		comment = re.findall('<span class="stats-comments">.*?class="number">(.*)</i>',story,re.S)
		# 判断是否存在评论，不存在则赋值为0
		if comment:
			comment = comment[0].strip()
		else:
			comment = str(0)
		# authour是一个段子的发布者，contxt是内容，good是点赞，comment是评论数
		return [authour, contxt, good, comment]
		# print(authour.strip(), contxt.strip(), good.strip(), comment.strip())
		# print(len(pageStories))


	# 传入某一页代码，返回本页不带图片的段子列表
	def getPageItems(self, pageIndex):
		pageCode = self.getPage(pageIndex)
		if not pageCode:
			print(u'页面加载失败....')
			return None
		# 先大后小，即先取一个个段子们，再去提取段子内容
		pattern = re.compile('<div class="article block untagged mb15".*?>(.*?)<div id="qiushi_counts_',re.S)
		storyList = re.findall(pattern, pageCode)
		# 用来存储每页的段子们
		pageStories = []
		# 用正则表达式去每个段子匹配细节信息
		for story in storyList:
			pageStories.append(self.getStoryDetail(story))
		return pageStories

	# 加载并提前页面的内容，加入到列表中
	def loadPage(self):
		# 如果当前未看的页数少于2页，则加载新一页
		if self.enable == True:
			if len(self.stories) < 2:
				# 获取新一页
				pageStories = self.getPageItems(self.pageIndex)
				# 将该业的段子存放到全局变量list中
				if pageStories:
					self.stories.append(pageStories)
					# 获取完之后页码索引加一，表示下次读取下一页
					self.pageIndex += 1


	# 调用该方法，每次敲回车打印一个段子
	def getOneStory(self, pageStories, page):
		# 遍历每一页的段子
		for story in pageStories:
			# 等待用户输入
			input = raw_input()
			# 每当输入回车一次，判断一下是否要加载新页面
			self.loadPage()
			# 如果输入Q则程序结束
			if input == 'Q':
				self.enable = False
				return
			print(u'第%d页\t发布人：%s\t好笑：%s\t评论：%s\n%s' %(page, story[0], story[2],story[3], story[1]))

	# 开始方法
	def start(self):
		print(u'正在读取糗事百科，按回车查看新段子，Q退出')
		# 使变量为True，程序可以正常运行
		self.enable = True
		# 先加载一页内容
		self.loadPage()
		# 局部变量，空值当前读到了第几页
		nowPage = 0
		while self.enable:
			if len(self.stories) > 0:
				# 从全局list中获取一页的段子
				pageStories = self.stories[0]
				# 当前读到的页数加一
				nowPage +=1
				# 将全局lis中的第一个元素删除，因为已经取出
				del self.stories[0]
				# 输出该页的段子
				self.getOneStory(pageStories, nowPage)

if __name__ == '__main__':

	spider = QSBK()
	spider.start()
	# list = spider.getPageItems(1)
	# for each in list:
	# 	for item in each:
	# 		print item,
	# 	print("")
