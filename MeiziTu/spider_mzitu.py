# coding=utf-8
'''
Created on 2017年3月8日
@author: Gym
@content: 爬取'mzitu.com'网站上的图片
'''
import urllib
import urllib2
import re
import os

class Spider:
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.number = 0  # 已爬取的妹子页面数
        
    # 获取索引页面的内容
    def getPage(self, target_url):
        try:
            url = target_url
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"网页连接失败,错误原因", e.reason
                return None
    
    # 从主页面中获取所有二级页面的链接
    def getAllUrls(self, page):
        pattern = re.compile('<a href="http://www.mzitu.com/(.*?)" target="_blank">', re.S)
        urls = re.findall(pattern, page)
        count = 0
        result = []
        for url in urls:
            if len(url) <= 5:  # 取出代表真正网页链接的标签信息
                result.append(url)
                count += 1
        print 'page count =', count
        return result
    
    # 给定一个二级页面地址，获取页面标题与照片数
    def getTitleAndNum(self, target_url):
        url = target_url
        page = self.getPage(url)
        title_pattern = re.compile('<h2 class="main-title">(.*?)</h2>', re.S)
        title = re.search(title_pattern, page)
        num_pattern = re.compile('<span>(.*?)</span>', re.S)
        nums = re.findall(num_pattern, page)
        real_nums = []
        for num in nums:
            if len(num) < 3:  # 找到那些真正代表照片数的信息
                real_nums.append(num)
        return title.group(1).strip(), real_nums[-1]
    
    def getPageImgs(self, page_url, imgNums, page_title):
        self.mkdir(page_title)
        for i in range(imgNums):
            target_url = page_url + '/' + str(i)
            page = self.getPage(target_url)
            pattern = re.compile('<div class="main-image">.*?<img src="(.*?)".*?>', re.S)
            img_url = re.search(pattern, page)
            img_url = img_url.group(1).strip()
            splitPath = img_url.split('.')
            fTail = splitPath.pop()
            img_name = page_title + '/' + str(i) + '.' + fTail
            self.saveImg(img_url, img_name)
        
    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            # 如果不存在则创建该目录
            print "create dir named",
            print path
            print "Start downloading..."
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print u"dir named", path, 'has been created. Start downloading...'
            return False
        
    # 传入图片地址，文件名，保存单张图片
    def saveImg(self, imageURL, fileName):
        u = urllib.urlopen(imageURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        f.close()
    
    def start(self, maxNum):
        print 'Spider start working...'
        page = self.getPage(self.base_url)
        urls = self.getAllUrls(page)
        for i, item in enumerate(urls):
            page_url = 'http://www.mzitu.com/' + item
            page_title, page_nums = self.getTitleAndNum(page_url)
            print '\npage ' + str(i+1) + ' has ' + page_nums + ' pictures'
            self.getPageImgs(page_url, int(page_nums), page_title)
            self.number += 1
            if self.number >= maxNum:  # 爬取指定数目的页面，以免硬盘不够存
                break
        print '\nSpider finished.'
    
    
if __name__ == "__main__":
    S = Spider('http://www.mzitu.com/all')
    number = raw_input('How many pages do you want to get? Input a number:')
    S.start(int(number))
