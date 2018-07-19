#!/usr/bin/env python 
# -*- coding:utf-8 -*-

# 抓取妹子图每日更新网页的妹子图片保存在本地(2018年最新一个月的图片)
# 目标url http://www.mzitu.com/all/

import re
import urllib.request

from bs4 import BeautifulSoup


class SpiderMzitu(object):

    def getHtmlContent(self, src):
        if src is None:
            return
        # 如果不加上下面的这行出现会出现urllib2.HTTPError: HTTP Error 403: Forbidden错误
        # 主要是由于该网站禁止爬虫导致的，可以在请求加上头信息，伪装成浏览器访问User-Agent,具体的信息可以通过火狐的FireBug插件查询
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = urllib.request.Request(url=src, headers=headers)
        response = urllib.request.urlopen(req)
        if response.getcode() != 200:
            return
        return response.read()

    def getDatas(self, html_cont):
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        all = soup.find('div', class_='all').find_all('a')
        for a in all:
            secSrc = a['href']
            if secSrc == "http://www.mzitu.com/old/":
                continue
            print('secSrc=== ', secSrc)
            secHtmlCont = self.getHtmlContent(secSrc)
            secSoup = BeautifulSoup(secHtmlCont, 'html.parser', from_encoding='utf-8')
            pages = secSoup.find('div', class_="pagenavi").find_all('span')
            index = 1
            while index < (len(pages) - 2):
                targetSrc = secSrc + '/' + str(index)
                targetHtmlCont = self.getHtmlContent(targetSrc)
                targetSoup = BeautifulSoup(targetHtmlCont, 'html.parser', from_encoding='utf-8')
                image = targetSoup.find('div', class_='main-image').find('img')
                name = image['alt'] + str(index)
                url = image['src']
                print('开始下载:\n,第%d张: %s  %s' % (index, url, name))
                opener = urllib.request.build_opener()
                opener.addheaders = [('Referer', "http://www.mzitu.com"), ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(url, './mzitu/%s.jpg' % name)
                index += 1
        print('下载完成------------')


    def spide(self, src):
        html_content = self.getHtmlContent(src)
        self.getDatas(html_content)


if __name__ == '__main__':
    src = 'http://www.mzitu.com/all/'
    spider = SpiderMzitu()
    spider.spide(src)
