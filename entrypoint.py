from jinglan.conf import conf

name = conf.PROJECT_NAME

from scrapy.cmdline import execute
execute(['scrapy', 'crawl', name])