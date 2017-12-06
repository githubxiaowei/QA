import xml.sax
import sys

class XmlHandler( xml.sax.ContentHandler ):
	def __init__(self):
		self.currentTag = ""
		self.text_id = 0
		self.currentTitle = ''
		self.fileOut = ''


	# 元素开始事件处理
	def startElement(self, tag, attributes):
		if(tag == 'text'):
			self.text_id += 1
			fpath = 'pages/'+str(self.text_id>>16 & 255)+'/'+str(self.text_id>>8 & 255)+'/'+str(self.text_id&255)
			sys.stdout.write(fpath+'\r')
			self.fileOut = open(fpath,'w',encoding='utf8')
			self.fileOut.write('title|'+self.currentTitle+'\n')
		self.currentTag = tag


	# 元素结束事件处理
	def endElement(self, tag):
		if(tag == 'text'):
			self.fileOut.close()
		self.currentTag = ''



	# 内容事件处理
	def characters(self, content):
		if(self.currentTag == 'title'):
			self.currentTitle = content
		if(self.currentTag == 'text'):
			self.fileOut.write(content)
  
if ( __name__ == "__main__"):

	import os, sys

	for i in range(256):
		for j in range(256):
			os.makedirs('./pages/'+str(i)+'/'+str(j))
	
	# 创建一个 XMLReader
	parser = xml.sax.make_parser()
	# turn off namepsaces
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)

	# 重写 ContextHandler
	Handler = XmlHandler()
	parser.setContentHandler( Handler )

	
	try:
		parser.parse("../QA_bak/zhwiki-20171020-pages-articles-multistream.xml")
	except Exception as e:
		print(e)
