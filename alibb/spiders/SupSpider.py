# -*- coding: UTF-8 -*-
import scrapy
from alibb.items import SupItem
import urllib
from scrapy import log
import sys
from json import decoder
from alibb import pooled
reload(sys)
sys.setdefaultencoding('utf-8')
class SupSpider(scrapy.Spider):
    name = 'sup'
    allowed_domains = ['1688.com']
    start_urls = ["http://s.1688.com"]
    zjCity = ['杭州','宁波','温州','绍兴','台州','嘉兴','金华','丽水','湖州','衢州','舟山']
    gzCity = ['广州','深圳','珠海','潮州','中山','东莞','佛山','惠州','汕头','汕尾','韶关','湛江','肇庆','河源','江门','揭阳','茂名','梅州','清远','阳江','云浮']
    provinces = ['广东','浙江','江苏','山东','河北','河南','福建','辽宁','安徽','广西','山西','海南','内蒙','吉林','黑龙','湖北','湖南','江西','宁夏','新疆','青海','陕西','甘肃','四川','云南','贵州','西藏','台湾','香港','澳门']
    conn = pooled.conn

    def parse(self, response):
        print sys.path[0]
        words = []
        with open('words.txt','r') as f:
            for line in f.readlines():
                words.append(line.strip().decode('utf-8'))

        webformat = "http://s.1688.com/selloffer/offer_search.htm?uniqfield=userid&from=marketSearch&n=y&filt=y&sortType=pop"
        params = "&city=%s&province=%s&keywords=%s"

        print '^^^^^^^^^^^', words
        for word in words:
            print u'开始处理word:', word
            for province in self.provinces:
                if province == '浙江':
                    for city in self.zjCity:
                        provinceParam = urllib.quote(u'浙江'.encode('gbk'))
                        cityParam = urllib.quote(city.decode('utf-8').encode('gbk'))
                        wordParam = urllib.quote(word.encode('gbk'))
                        web = params % (cityParam, provinceParam, wordParam)
                        web = webformat + web
                        url = web + "&biztype=1"
                        print '########################################hz 1'
                        yield scrapy.Request(url, meta={'word':word}, callback=self.parse_search_page)
                        url = web + "&biztype=2"
                        print '##################################hz 2'
                        yield scrapy.Request(url, meta={'word':word}, callback=self.parse_search_page)
                        url = web + "&biztype=4"
                        print '#######################################hz 4'
                        yield scrapy.Request(url, meta={'word':word}, callback=self.parse_search_page)
                        url = web + "&biztype=8"
                        print '#############################################hz 8'
                        yield scrapy.Request(url, meta={'word':word}, callback=self.parse_search_page)
                        url = web
                        print '############################################hz all'
                        yield scrapy.Request(url, meta={'word':word}, callback=self.parse_search_page)
                elif province == '广州':
                    for city in self.gzCity:
                        provinceParam = urllib.quote(u'广州'.encode('gbk'))
                        cityParam = urllib.quote(city.decode('utf-8').encode('gbk'))
                        wordParam = urllib.quote(word.decode('utf-8').encode('gbk'))
                        web = params % cityParam, provinceParam, wordParam
                        web = webformat + web
                        url = web + "&biztype=1"
                        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$gz 1'
                        yield scrapy.Request(url, meta={'word':word}, callback=self.parse_search_page)
                        url = web + "&biztype=2"
                        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$gz 2'
                        yield scrapy.Request(url, meta={'word':word}, callback=self.parse_search_page)
                        url = web + "&biztype=4"
                        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$gz 4'
                        yield scrapy.Request(url, meta={'word':word}, callback=self.parse_search_page)
                        url = web + "&biztype=8"
                        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$gz 8'
                        yield scrapy.Request(url, meta={'word':word}, callback=self.parse_search_page)
                        url = web
                        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$gz all'
                        yield scrapy.Request(url, meta={'word':word}, callback=self.parse_search_page)
                else:
                    provinceParam = urllib.quote(province.decode('utf-8').encode('gbk'))
                    wordParam = urllib.quote(word.encode('gbk'))
                    web = "&province=%s&keywords=%s" % (provinceParam, wordParam)
                    web = webformat + web
                    url = web
                    yield scrapy.Request(url, meta={'word':word}, callback=self.parse_search_page)

    def parse_search_page(self, response):
        sel = scrapy.Selector(response)
        links = sel.xpath("//div[@class='sm-offerShopwindow-company fd-clr']").xpath("a[@class='sm-previewCompany sw-mod-previewCompanyInfo']/attribute::href")
        for link in links:
            url = link.extract()
            print 'begin select link ----------------------------', url
            row = SupSpider.conn.get('select * from alibb where website=%s', url)
            if row:
                print u'已经存在该记录，不再处理------------------------------------------->'
                continue
            print '查询详情<<<<<<<<<<<<<<<<<<<<<<<<<<<<'.decode('utf-8'), url, ',word:', response.meta['word']
            yield scrapy.Request(url + "/page/creditdetail.htm", meta={'word':response.meta['word'], 'link': url},callback=self.parse_detail)
            print '11111111111111111111111111111111111111111'
            yield scrapy.Request(url + "/page/creditdetail_remark.htm" , meta={'word':response.meta['word'], 'link':url}, callback=self.parse_exchange_detail)
            print '2222222222222222222222'
        page_max = sel.xpath("//form[@id='sw_mod_pagination_form']//input[@name='beginPage']/@data-max").extract()
        print '\n\n3333333333333333333333333333333pageMax:', page_max

        if page_max:
            print '\n\n\n\n\n翻页\n'.decode('utf-8'),'word:', response.meta['word']
            page_no = response.meta['pageNo'] if 'pageNo' in response.meta else 0
            page_max = int(page_max[0])
            print '\n\npageno:',page_no, '\n\npagemax:',page_max
            if not page_no:
                print '@@@@@@@@@@@@@@@@@@@2打印第二页'.decode('utf-8')
                url = response.url + '&beginPage=2'
                yield scrapy.Request(url, meta={'word': response.meta['word'], 'url': response.url, 'pageNo': 2}, callback=self.parse_search_page)
            elif page_no < page_max:
                print '@@@@@@@@@@@@@@@@@@2222打印下一页'.decode('utf-8'), page_no
                url = response.meta['url']
                page_no += 1
                url = url + '&beginPage=' + str(page_no)
                yield scrapy.Request(url, meta={'word': response.meta['word'], 'url': response.meta['url'], 'pageNo': page_no}, callback=self.parse_search_page)
        else:
            print '\n\n\n444444444444444444444444444444444444'

    def parse_detail(self, response):
        """
        处理详情页
        :param response:
        :return:
        """

        print 'deal with detail page>>>>>>>>>>>>>>>>>>>>>>>>>>>,word:',response.meta['word']

        item = SupItem()
        item['word'] = response.meta['word']

        sel = scrapy.Selector(response)
        name = sel.xpath("//div[@class='archive-base-info fd-clr']//dl/dd[1]/@title").extract()
        # print 'name:', name
        mobile = sel.xpath("//div[@class='archive-base-info fd-clr']//dl/dd[2]/text()").extract()
        # print 'mobile:', mobile
        tel = sel.xpath("//div[@class='archive-base-info fd-clr']//dl/dd[3]/text()").extract()
        # print 'tel:', tel
        level = sel.xpath("//div[@class='medal']/a/img/@src").extract()
        # print 'level:', level
        honest = sel.xpath("//span[@class='state-cxt']/em/text()").extract()
        # print 'honest:', honest
        buildDate = sel.xpath("//div[@class='company-info fd-clr']/ul[1]/li[1]/text()").extract()
        # print buildDate
        area = sel.xpath("//div[@class='company-info fd-clr']/ul[1]/li[2]/span[2]/@title").extract()
        # print area
        address = sel.xpath("//div[@class='company-info fd-clr']/ul[2]/li[2]/text()").extract()
        # print 'address:', address
        company = sel.xpath("//div[@id='archive-base-info']//h2[@class='company-title']/span[1]/@title").extract()
        # print 'company:', company



        item['website'] = response.meta['link'] #str(response.url).encode('utf-8')
        if name:
            item['name'] = name[0]
        if mobile:
            item['mobile'] = mobile[0]
        if tel:
            item['tel'] = tel[0]
        if level:
            item['level'] = level[0]
        if honest:
            item['honest'] = honest[0]
        if buildDate:
            item['buildDate'] = buildDate[0]
        if area:
            item['area'] = area[0]
        if address:
            item['address'] = address[0]
        if company:
            item['company'] = company[0]

        return item

    def parse_exchange_detail(self, response):
        sel = scrapy.Selector(response)
        memberId = sel.xpath("//input[@id='feedbackUid']/@value").extract()
        if not memberId:
            return
        url = """http://rate.1688.com/remark/viewPubRemark/view.json?callback=f&_input_charset=UTF-8&memberId=%s&tradeType=ALL&memberRole=seller&needDsr=false&showList=false"""
        url = url % memberId[0]
        yield scrapy.Request(url, meta={'word': response.meta['word'], 'link': response.meta['link']}, callback=self.parse_rate)




        # sel = scrapy.Selector(response)
        #
        # tr = sel.xpath("//dd[@class='pj-score-right module-a']//table/tbody/tr[6]")
        # lastOneWeek = tr.xpath("td[2]/a/text()").extract()
        # lastOneMonth = tr.xpath("td[3]/a/text()").extract()
        # lastSixMonth = tr.xpath("td[4]/a/text()").extract()
        # beforeHalfYear = tr.xpath("td[5]/a/text()").extract()
        # total = tr.xpath("td[6]/a/text()").extract()
        #
        # item = SupItem()
        # item['website'] = response.meta['link']
        # item['word'] = response.meta['word']
        # if lastOneWeek:
        #     item['lastOneWeek'] = lastOneWeek[0]
        # if lastOneMonth:
        #     item['lastOneMonth'] = lastOneMonth[0]
        # if lastSixMonth:
        #     item['lastSixMonth'] = lastSixMonth[0]
        # if beforeHalfYear:
        #     item['beforeHalfYear'] = beforeHalfYear[0]
        # if total:
        #     item['total'] = total
        #
        # return item
        # print "查看交易记录".decode('utf-8')


    def parse_rate(self, response):
        item = SupItem()
        item['website'] = response.meta['link']
        item['word'] = response.meta['word']
        json = response.body[response.body.find('{'):-2]
        print 'json->>>>>>>>>>>>>>>>>>>>>>>', json
        jsonD = decoder.JSONDecoder()
        djson = jsonD.decode(json)
        item['lastOneWeek'] = djson['data']['starStatisticsList'][5]['weekly']
        item['lastOneMonth'] = djson['data']['starStatisticsList'][5]['monthly']
        item['lastSixMonth'] = djson['data']['starStatisticsList'][5]['halfYearly']
        item['beforeHalfYear'] = djson['data']['starStatisticsList'][5]['halfYearBefore']
        item['total'] = djson['data']['starStatisticsList'][5]['totals']
        return item

