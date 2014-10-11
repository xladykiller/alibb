# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from alibb import pooled
import time
class TestPipeline(object):
    def process_item(self, item, spider):
        return item


class SupPipeline(object):
    conn = pooled.conn
    def process_item(self, item, spider):
        print '>>>>>>>>>>>>>>>>>>>>>>>!!!!!!!!!!!!!!!!!!!!!!!!!!111'

        if item['website']:
            print item['website']
            row = SupPipeline.conn.get("select * from alibb where website=%s",item['website'])
            if row:
                params = []
                update = 'update alibb set website=%s'
                params.append(item['website'])
                if 'word' in item:
                    update += ',word=%s'
                    params.append(item['word'])
                if 'name' in item:
                    update += ',name=%s'
                    params.append(item['name'])
                if 'company' in item:
                    update += ',company=%s'
                    params.append(item['company'])
                if 'mobile' in item:
                    update += ',mobile=%s'
                    params.append(item['mobile'])
                if 'tel' in item:
                    update += ',tel=%s'
                    params.append(item['tel'])
                if 'level' in item:
                    update += ',level=%s'
                    params.append(item['level'][item['level'].rfind('/')+1:])
                if 'honest' in item:
                    update += ',honest=%s'
                    params.append(item['honest'])
                if 'buildDate' in item:
                    update += ',build_date=%s'
                    params.append(item['buildDate'].strip().replace('年', '-').replace('月', '-').replace('日', ''))
                if 'area' in item:
                    update += ',area=%s'
                    params.append(item['area'])
                if 'address' in item:
                    update += ',address=%s'
                    params.append(item['address'])

                if 'lastOneWeek' in item:
                    update += ',last_one_week=%s'
                    params.append(item['lastOneWeek'])
                if 'lastOneMonth' in item:
                    update += ',last_one_month=%s'
                    params.append(item['lastOneMonth'])
                if 'lastSixMonth' in item:
                    update += ',last_six_month=%s'
                    params.append(item['lastSixMonth'])
                if 'beforeHalfYear' in item:
                    update += ',before_half_year=%s'
                    params.append(item['beforeHalfYear'])
                if 'total' in item:
                    update += ',total=%s'
                    params.append(item['total'])

                update += ', upd_tm=%s where website=%s '
                params.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                params.append(item['website'])
                print '------------------>', update,'------------>\n', params
                SupPipeline.conn.update(update, *tuple(params))
            else:
                params = []
                vals = []
                head = 'insert into alibb (%s)'
                insert = ' values ('
                vals.append('website')
                params.append(item['website'])
                insert += '%s'

                vals.append(',ins_tm')
                params.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                insert += ',%s'

                vals.append(',upd_tm')
                params.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                insert += ',%s'

                if 'word' in item:
                    insert += ',%s'
                    vals.append(',word')
                    params.append(item['word'])
                if 'name' in item:
                    insert += ',%s'
                    vals.append(',name')
                    params.append(item['name'])
                if 'company' in item:
                    insert += ',%s'
                    vals.append(',company')
                    params.append(item['company'])
                if 'mobile' in item:
                    insert += ',%s'
                    vals.append(',mobile')
                    params.append(item['mobile'])
                if 'tel' in item:
                    insert += ',%s'
                    vals.append(',tel')
                    params.append(item['tel'])
                if 'level' in item:
                    insert += ',%s'
                    vals.append(',level')
                    params.append(item['level'][item['level'].rfind('/')+1:])
                if 'honest' in item:
                    insert += ',%s'
                    vals.append(',honest')
                    params.append(item['honest'])
                if 'buildDate' in item:
                    insert += ',%s'
                    vals.append(',build_date')
                    params.append(item['buildDate'].strip().replace('年', '-').replace('月', '-').replace('日',''))
                if 'area' in item:
                    insert += ',%s'
                    vals.append(',area')
                    params.append(item['area'])
                if 'address' in item:
                    insert += ',%s'
                    vals.append(',address')
                    params.append(item['address'])

                if 'lastOneWeek' in item:
                    insert += ',%s'
                    vals.append(',last_one_week')
                    params.append(item['lastOneWeek'])
                if 'lastOneMonth' in item:
                    insert += ',%s'
                    vals.append(',last_one_month')
                    params.append(item['lastOneMonth'])
                if 'lastSixMonth' in item:
                    insert += ',%s'
                    vals.append(',last_six_month')
                    params.append(item['lastSixMonth'])
                if 'beforeHalfYear' in item:
                    insert += ',%s'
                    vals.append(',before_half_year')
                    params.append(item['beforeHalfYear'])
                if 'total'  in item:
                    insert += ',%s'
                    vals.append(',total')
                    params.append(item['total'])

                insert += ')'
                sql = head % ''.join(vals)
                sql += insert
                print 'sql:-------------->', sql
                print 'len of params------------->', tuple(params)

                SupPipeline.conn.insert(sql, *tuple(params))
            print u'\n\n\n打印查询完的数据库>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            print "row is \n-----------------------------\n",row
        return item