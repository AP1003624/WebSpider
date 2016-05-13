# coding=utf8
# Create by 吴俊 on 2016/5/12

import re


# 去除文本中html标签并保留原格式工具类
# 使用方法：
# # from Tool import *
# # tool = Tool()
# # tool.replaceHTMLTag(html)
class Tool:
	def __init__(self):
		# 去除img标签，1-7位长空格
		self.removeImg = re.compile(u'<img.*?>| {1,7}|&nbsp;')
		# 删除超链接标签
		self.removeAddr = re.compile(u'<a.*?>|</a>')
		# 把换行的标签换为\n
		self.repalceLine = re.compile(u'<tr>|<div>|</div>|</p>')
		# 将表格制表<td>替换为\t
		self.repalceTD = re.compile(u'<td>')
		# 把段落开头换为\n加两空格
		self.repalcePara = re.compile(u'<p.*?>')
		# 将换行符或双换行符替换为\n
		self.repalceBR = re.compile(u'<br><br>|<br>')
		# 将其余标签剔除
		self.repalceExtraTag = re.compile(u'<.*?>')

	def replaceHTMLTag(self, html):
		html = re.sub(self.removeImg, "", html)
		html = re.sub(self.removeAddr, "", html)
		html = re.sub(self.repalceLine, "\n", html)
		html = re.sub(self.repalceTD, "\t", html)
		html = re.sub(self.repalcePara, "\n  ", html)
		html = re.sub(self.repalceBR, "\n", html)
		html = re.sub(self.repalceExtraTag, "", html)
		# strip()将前后多余内容删除
		return html.strip()


if __name__ == '__main__':
	print(u'这是一个去除文本中html标签并保留原格式工具类')
