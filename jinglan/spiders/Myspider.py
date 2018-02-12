# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class Myspider(scrapy.Spider):
    name = 'jinglan'
    allowed_domains = ['23wx.cc']
    bash_url = 'http://23wx.cc/class/'
    bashurl = '.html'

    def parse(self, response):
        for i in range(1,11):
            url = self.bash_url + str(i) + '_1' + self.bashurl
            yield Request(url, self.parse)
