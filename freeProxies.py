#! usr/bin/env python3
# -*- coding:utf-8 -*-
import requests
import re

class mainSpider(object):
    def __init__(self):
        print("开始获取代理........")


    # 初始化URL并获取待爬取列表
    def getPage(self, totalPage):
        initUrl = 'http://www.xicidaili.com/nn/'
        pageGroup = []
        for i in range(1, totalPage):
            link = initUrl + str(i)
            pageGroup.append(link)
        return pageGroup


    # 获取源码
    def getSource(self, url):
        initHeader = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
            "Referer": "http://www.xicidaili.com/nn/"
        }
        html = requests.get(url, headers= initHeader)
        htmlSourceCode = html.text
        return htmlSourceCode


    # 获取class="odd"这部分内容,默认从cn截取
    def getOddCn(self, htmlSourceCode):
        oddCn = re.findall('alt="Cn" /></td>(.*?)</tr>', htmlSourceCode, re.S)
        return oddCn


    # 取出IP,port
    def getProxy(self, getIPs):
        proxyDict = {}
        proxyDict['IP'] = re.findall('<td>(.*?)</td>', getIPs)[0]
        proxyDict['Port'] = re.findall('<td>(.*?)</td>', getIPs)[1]
        return proxyDict


    # 保存为文本文件
    def saveProxy (self, proxyList):
        f = open('freeProxies.txt', 'a')
        for eachProxy in proxyList:
            f.writelines(eachProxy['IP'] + ':' + eachProxy['Port'] + '\n')
        f.close()



if __name__ == '__main__':
    proxyList = []
    freeProxies = mainSpider()
    allLinks = freeProxies.getPage(3) #在这里填写页数,不推荐写太多,有些IP会失效
    for link in allLinks:
        print("正在获取" + link + "的高匿代理")
        htmlSourceCode = freeProxies.getSource(link)
        oddCn = freeProxies.getOddCn(htmlSourceCode)
        for eachOdd in oddCn:
            eachProxy = freeProxies.getProxy(eachOdd)
            proxyList.append(eachProxy)
    freeProxies.saveProxy(proxyList)
    print("爬取完毕")
