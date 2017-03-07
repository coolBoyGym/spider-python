# -*- coding:utf-8 -*-
'''
Created on 2016年9月1日
@author: Gym
@input: 百度贴吧某个帖子的代号和本地文件夹名称
@output: 该帖子里楼主所上传的图片(下载到本地)
'''
import urllib
import urllib2
import re
import os

class Spider:
    # 页面初始化
    def __init__(self, target_url):
        self.siteURL = target_url
        self.pictureNum = 0
    
    # 获取索引页面的内容
    def getPage(self, pageNum):
        try:
            url = self.siteURL + '?see_lz=1' + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # 返回最原始的HTML代码，与浏览器中使用F12键来查看的可能会有些不同
            # 可以把页面打印到本地中来查看
            # 或者直接在页面右击：查看网页源码 来查看
            return response.read()
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接百度贴吧失败,错误原因", e.reason
                return None
    
    #获取帖子总页数
    def getPageNum(self, page):
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None
        
    def getAllImg(self, page):
        # 编写正则表达式的规则是整个任务最重要的一步
        patternImg = re.compile('<img class="BDE_Image".*?src="(.*?)".*?">', re.S)
        images = re.findall(patternImg, page)
        # for img in images:
        #    print img
        return images
    
    # 创建新目录
    def mkdir(self, path):
        path = path.strip()
        # 判断路径是否存在
        # 存在返回True，不存在返回False
        isExists = os.path.exists(path)
        if not isExists:
            # 如果不存在则创建该目录
            print "create dir named",
            print path
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print u"名为", path, '的文件夹已经创建成功'
            return False
        
    def saveImgs(self, images, name):
        number = self.pictureNum
        for imageURL in images:
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            fileName = name + "/" + str(number) + "." + fTail
            self.saveImg(imageURL, fileName)
            number += 1
        self.pictureNum = number
            
    # 传入图片地址，文件名，保存单张图片
    def saveImg(self, imageURL, fileName):
        u = urllib.urlopen(imageURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        print u"正在保存她的一张图片为",
        print fileName
        f.close()
    
    def begin(self, name):
        print "Spider start working..."
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        self.mkdir(name)
        if pageNum == None:
            print "URL已失效, 请重试"
            return 
        try:
            print "该帖子共有" + str(pageNum) + "页"
            for i in range(1, int(pageNum) + 1):
                print "正在抓取第" + str(i) + "页图片"
                page = self.getPage(i)
                images = self.getAllImg(page)
                self.saveImgs(images, name)
        except IOError, e:
            print "写入异常, 原因:" + e.message
        finally:
            print "写入任务完成!" 
            print "总共爬取" + str(self.pictureNum) + "张图片"
            
        
if __name__ == '__main__':
    print u'请输入帖子代号'
    base_url = 'http://tieba.baidu.com/p/'
    target_url = base_url + str(raw_input('http://tieba.baidu.com/p/'))
    print u'请输入本地文件夹名称(英文)'
    filename = str(raw_input('filename='))
    spider = Spider(target_url)
    spider.begin(filename)
