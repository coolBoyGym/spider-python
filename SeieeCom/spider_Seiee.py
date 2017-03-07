# coding=utf-8
'''
Created on 2017年3月7日
@author: Gym
@summary: 从本地文件中读取学号信息，从z.seiee.com网站上得到对应信息，最后将所有信息写入本地文件中
@attention: 只有在Seiee网站开放查询的时候方可使用
@test: Eclipse + Pydev
'''
import urllib2
import re

url = 'http://z.seiee.com/scores/search?student_no=' 
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
f = open("E:/Downloads/CS.txt", "r", )
result = open("E:/Downloads/CSresult.txt", "w")

print 'Begin...'
try:
    s = f.readline()
    while s != '':
        l = s.split('\t')
        sno = l[1]
        Url = url + sno
        request = urllib2.Request(Url, headers=headers)
        response = urllib2.urlopen(request)
        content = response.read().decode('utf-8')
        pattern = re.compile('<td width="70%">(.*?)</td>', re.S)
        item = re.findall(pattern, content)
        result.write(l[0]+'\t'+item[0]+'\t'+sno+'\t'+l[3]+'\t'+l[4]+'\t'+l[5])
        s = f.readline()
        
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason
        
f.close()
result.close()
print 'Over'