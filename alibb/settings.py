# -*- coding: utf-8 -*-

# Scrapy settings for alibb project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'alibb'

SPIDER_MODULES = ['alibb.spiders']
NEWSPIDER_MODULE = 'alibb.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'alibb (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'alibb.pipelines.SupPipeline': 300
}

DOWNLOAD_DELAY = 1

COOKIES_ENABLED = False