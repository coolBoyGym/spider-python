# -*- coding:utf-8 -*-
'''
Created on 2016年3月27日
@author: Gym
@content: 贴吧爬虫，用于爬取百度贴吧某条帖子里所有楼层的文字内容
@usage: 安装python2.7，双击打开，根据提示依次输入相关信息，短暂等待后即可获取文字内容
'''
import sys
import urllib
import urllib2
import re

#处理页面标签类
class Tool:
	#去除空格
	#removeKongGe = re.compile('&nbsp;')
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    
    def replace(self,x):
		#x = re.sub(self.removeKongGe,"",x)
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()


#百度贴吧爬虫类
class BDTB:

    #初始化，传入基地址与是否只看楼主的参数
    def __init__(self, baseUrl, seeLZ, floorTag):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool = Tool()
        self.file = None
        self.floor = 1
        self.defaultTitle = u"百度贴吧"
        #是否写入楼分隔符的标记
        self.floorTag = floorTag
        

    #传入页码，获取该页帖子的代码
    def getPage(self, pageNum):
        try:
            url = self.baseURL+ self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            #返回utf-8格式编码内容
            return response.read().decode('utf-8')
        #无法连接网页,报错
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接百度贴吧失败,错误原因",e.reason
                return None
    
    #获取帖子标题
    def getTitle(self, page):
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None
    
    #获取帖子总页数
    def getPageNum(self, page):
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None
    
    #传入页面内容,获取每一楼层的内容
    def getContent(self, page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            #对文本进行去标签处理,同时在前后加入换行符
            content = "\n" + self.tool.replace(item) + "\n"
            contents.append(content.encode('utf-8'))
        return contents
    
    #创建保存内容的文件
    def setFileTitle(self, title):
        if title is not None:
            self.file = open(title + ".txt", "w+")
        else:
            self.file = open(self.defaultTitle + ".txt", "w+")
    
    def writeData(self, contents):
        #向文件写入每一楼的信息
        for item in contents:
            if self.floorTag == '1':
                floorLine = "\n" + str(self.floor) + u"楼------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1
    
    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print u"URL已失效,请重试"
            return 
        try:
            print ("该帖子共有" + str(pageNum) + "页").decode('utf-8').encode('gbk')
            for i in range(1, int(pageNum) + 1):
                print ("正在写入第" + str(i) + "页数据").decode('utf-8').encode('gbk')
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError, e:
            print ("写入异常, 原因:" + e.message).decode('utf-8').encode('gbk')
        finally:
            print u"写入任务完成!"

reload(sys)
sys.setdefaultencoding('utf-8')
print u"请输入帖子代号"
baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
seeLZ = raw_input("是否只获取楼主发言,是输入1,否输入0\n".decode('utf-8').encode('gbk'))
floorTag = raw_input("是否需要写入楼层信息,是输入1,否输入0\n".decode('utf-8').encode('gbk'))
bdtb = BDTB(baseURL, seeLZ, floorTag)
bdtb.start()
