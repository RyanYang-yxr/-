# coding=utf-8
import requests
import re
import Queue
import threading
import json
from lxml import etree
import os
from bs4 import BeautifulSoup as bs
import codecs
import time
import random
# import pprint
from pprint import pprint
import sys
from threading import stack_size
stack_size(32768*16)
reload(sys)
sys.setdefaultencoding('utf8')
__author__ = 'Ryan Yang'
__date__ = '2017/3/15 17:30'

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log.log',
                    filemode='a')


Que = Queue.Queue()
myLock = threading.Lock()


class DianPing(object):
    def __init__(self):
        print 'start...'

    def get_url(self, url):
        agent = [
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'

        ]
        headers = {
            "User-Agent": agent[random.randint(0, len(agent) - 1)],
            # 'Accept': 'application/json, text/javascript'
            # "Host": "portal.braniteljski-forum.com"
        }
        try:
            html = requests.get(url, timeout=30, headers= headers)
            html_etree = etree.HTML(html.content)
            return html_etree, html
        except Exception as e:
            print e

    def get_user_profile(self, url, merchant_id):
        merchant_id = merchant_id
        html_etree, html = self.get_url(url)
        soup = bs(html.content, 'lxml')
        username = html_etree.xpath('//h2[@class="name"]/text()')[0].replace('\n','').replace("  ",'')
        user_id = re.findall("member/(\d+)", url)[0]

        try:
            address = soup.find("span", class_="user-groun").text
        except Exception as e:
            print "啥也没有人员"
            # address = ''
            raise e

        try:
            gender = soup.find("span", class_="user-groun").find("i")["class"][0]
        except Exception as e:
            # print "三无用户"
            gender = ''
            info = {'用户ID': user_id, '店铺ID': merchant_id, '用户名': username, '地址': address, '性别': gender, '恋爱状况': '', '星座': '', '生日': ''}
            info = json.dumps(info, ensure_ascii=False)
            return info

        try:
            base_info = soup.find(id='J_UMoreInfoD').find('ul').text
        except Exception as e:
            # print "无基本信息"
            # print e
            base_info = ''

        # print user_id
        # print username
        # print gender
        # print address
        # print base_info

        if base_info == '':
            info = {'用户ID': user_id, '店铺ID': merchant_id, '用户名': username, '地址': address, '性别': gender, '恋爱状况': '', '星座': '', '生日': ''}
            info = json.dumps(info, ensure_ascii=False)
            return info


        try:
            birthday = re.search(u'生日：(.*)', base_info).group(1)
        except Exception as e:
            # print "无生日"
            # print e
            birthday = ''
        # print birthday

        try:
            sign = re.search(u'星座： (.*)', base_info).group(1)
        except Exception as e:
            # print "无星座"
            # print e
            sign = ''
        # print sign

        try:
            relationship = re.search(u'恋爱状况：(.*)', base_info).group(1)
        except Exception as e:
            # print "无恋爱"
            # print e
            relationship = ''
        # print relationship

        info = {'用户ID': user_id, '店铺ID': merchant_id, '用户名': username, '地址': address, '性别': gender, '恋爱状况': relationship, '星座': sign, '生日': birthday}
        info = json.dumps(info, ensure_ascii=False)

        return info



    def save(self, info):
        # 定义目标文件保存的位置
        try:
            f = codecs.open('restaurants/guangzhou_canting.json', 'a+', 'utf-8')
        except:
            # 如果没有该目标文件夹，则创建一个
            os.mkdir('restaurants')
            f = codecs.open('restaurants/guangzhou_canting.json', 'a+', 'utf-8') 
        f.write(info + "\n")
        f.close()

    def main(self, f):
        global myLock
        i = 1
        while True:
            line = f.readline()
            if not line:
                break
            try:
                print i
                # print line
                # link = dict(line)["url"]
                # dictionary update sequence element #0 has length 1; 2 is required
                link = json.loads(line)["user_url"]
                merchant_id = re.findall('shop/(\d+)/review', json.loads(line)['shop_url'])[0]
                # print link
                info = self.get_user_profile(link, merchant_id)
            except Exception as e:
                print e
                print "获取内容失败"
                # print link
                print line
                print i
                print "***************"
                continue
            myLock.acquire()
            self.save(info)
            myLock.release()
            # time.sleep(5)
            i += 1




if __name__ == '__main__':
    spider = DianPing()
    # 这里选择要打开的目标文件的位置
    f = open('b_c/one_page.json_.json','r')
    # 创建20个线程
    ts = []
    for num in range(1, 20):
        t = threading.Thread(target=spider.main, args=(f,))
        t.start()
        # t.setDaemon(False)
        ts.append(t)

    for t in ts:
        t.join()

    f.close()
    # list_dirs = os.walk('./')

    print '----------------------THE END-------------------------'
    logging.info('----------------------THE END-------------------------')

# 上面的主函数一次只能解析一个文件，下面的备用主函数可遍历当前目录下所有目标文件，并解析
# if __name__ == '__main__':
#     spider = DianPing()
      # 定义要遍历的文件夹初始位置
#     list_dirs = os.walk('./')
#     # print list_dirs
#     for root,dirs,files in list_dirs:
#         for ff in files:
              # 拼凑目标文件路径
#             f_path = os.path.join(root, ff)
              # 如果目标文件名称符合要求，则执行函数
#             if ff == 'one_page.json_.json' or ff =='three_page.json_.json':
#                 # print ff
#                 # print f_path
#                 with open(f_path, 'r') as f:
                      # 在这里创建20个线程
#                     ts = []
#                     for num in range(1, 20):
#                         t = threading.Thread(target=spider.main, args=(f,))
#                         t.start()
#                         # t.setDaemon(False)
#                         ts.append(t)

#                     for t in ts:
#                         t.join()
#             else:
#                 continue

#     print '----------------------THE END-------------------------'
#     logging.info('----------------------THE END-------------------------')

