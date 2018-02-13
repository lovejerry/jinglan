import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from jinglan.items import JinglanItem


class Myspider(scrapy.Spider):
    name = 'jinglan'
    allowed_domains = ['23wx.cc']
    bash_url = 'http://23wx.cc/class/'
    bashurl = '.html'

    def start_requests(self):
        # for i in range(1, 11):
        #     url = self.bash_url + str(i) + '_1' + self.bashurl
        #     yield Request(url, self.parse)
        yield Request('http://www.23wx.cc/quanben/1', self.parse)

    # def parse(self, response):
    #     print("response.url: " + response.url)

    def parse(self, response):
        max_num = BeautifulSoup(response.text, 'lxml').find('div', class_='pagelink').find_all('a')[-1].get_text()
        # bashurl = str(response.url)[:-7]
        bashurl = str(response.url)[:-1]
        print("response.url: "+response.url)
        print("max_num: "+max_num)
        print("response.url.bashurl: " + bashurl)
        for num in range(1, int(max_num)+1):
        # for num in range(1, 3):
            # url = bashurl + '_' + str(num) + self.bashurl
            url = bashurl + str(num)
            yield Request(url, callback=self.get_name)
        # print(response.text)

    def get_name(self, response):
        # tds = BeautifulSoup(response.text, 'lxml').find_all('tr', bgcolor='#FFFFFF')
        tds = BeautifulSoup(response.text, 'lxml').find_all('td', class_='odd')
        for td in tds:
            # 这里用循环是因为find_all取出来的标签是以列表形式存在的：不然没法继续使用find
            print(td)
            print(td.find('a'))
            if td.find('a') is None:
                return
            novelname = td.find('a').get_text()
            novelurl = td.find('a')['href']
            print(novelurl)
            print(novelname)
            yield Request(novelurl, callback=self.get_chapterurl, meta={'name':novelname,'url':novelurl})

    def get_chapterurl(self, response):
        item = JinglanItem()
        item['name'] = str(response.meta['name'].replace('\xa0',''))
        item['novelurl'] = response.meta['url']
        # print(response.text)
        dds = BeautifulSoup(response.text, 'lxml').find('div', id='list').find_all("dd")
        # print(dds)
        category = ''
        for dd in dds:
            # print(dd.find('a').get_text())
            category = category + "," + dd.find('a').get_text()
        print(category)
        length = len(category)
        category = category[1:length]
        # category = '第一章 罪恶之城,第二章 火力凶猛'
        print(category)
        # 将字符串头部的，去掉
        author = BeautifulSoup(response.text, 'lxml').find('div', id='info').find('p').get_text();
        print(author)
        # 同样作者字符串需要处理
        # bash_url = BeautifulSoup(response.text, 'lxml').find('p', class_='btnlinks').find('a', class_='read')['href']
        # bash_url = BeautifulSoup(response.text, 'lxml').find('meta', property='og:url').attrs['content']
        bash_url = response.meta['url']
        print(bash_url)
        # name_id = str(bash_url)[-6:-1].replace('/','')
        name_id = bash_url
        item['category'] = str(category).replace('/', '')
        item['author'] = str(author).replace('/','')
        item['name_id'] = name_id
        return item
