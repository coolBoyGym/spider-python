# coding=utf-8
'''
Created on 2016年3月27日
@author: Gym
@summary: 从百度百科中Python词条页面出发，获取页面中的链接，并得到链接页面下的地址、标题以及简介三个信息
@usage: Eclipse + Pydev
'''
from baike_python import url_manager, html_downloader, html_parser, html_outputer

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
    
    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print 'craw %d : %s' % (count, new_url)
                html_cont = self.downloader.download(new_url)
                new_urls,new_data = self.parser.parse(new_url,html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)
                
                # 仅仅爬取20个页面作为测试
                if count ==20:
                    break
                count = count + 1
            except:
                print 'craw failed'
        
        self.outputer.output_html()
    

if __name__=="__main__":
    print "Spider begin working..."
    root_url = "http://baike.baidu.com/view/21087.htm"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
    print "Over"
    
    