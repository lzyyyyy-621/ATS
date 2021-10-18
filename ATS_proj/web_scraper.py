#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
from lxml import etree
import time
import random
import os
import json

headers = {
    'accept-language': 'zh-CN,zh;q=0.9',
    'origin': 'https://blog.csdn.net',
    'referer': 'https://blog.csdn.net/qq_39802740/article/details/89884756',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}

# 1. 同花顺
months = ["202005","202006","202007","202008","202009","202010", "202011", "202012", '202101', '202102', '202103', '202104', '202105', '202106', '202107', '202108', '202109', '202110']
days = [("0"+str(i))[-2:] for i in range(1, 32)]
links = [] # create links to visit
for m in months:
    for d in days:
        links.append("http://stock.10jqka.com.cn/zaopan/"+m+d+".shtml" )
# links[:3]

di = {}
for t, link in enumerate(links):
    date = link.split("/")[-1][:8]
    if t%30==0:
        print(date)
        time.sleep(5+ 5*random.random())
    r = requests.get(link, headers = headers)
    html = r.content
    selector = etree.HTML(html)
    xpath_list = selector.xpath('//div[@id="block_2125"]/p')
    text_list = [i.xpath('string(.)').strip() for i in xpath_list]
    di[date] = text_list


os.chdir("E:\\！研三上\\00 讲座课ML\\")
# save & read

# with open("tonghuashun.json", 'w') as f:
#     json.dump(di, f)
# with open("tonghuashun.json", 'r') as f:
#     di = json.load(f)



# 2. 上海证券报
# to solve anti web scraping, we use proxies and change headers
from faker import Factory
fc = Factory.create()  # create new headers each time

requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数

# https://ip.ihuan.me/
ips = """
117.94.222.142:3256
60.167.133.181:1133
60.167.82.129:1133
118.117.189.202:3256
121.232.148.78:3256
121.232.148.119:3256
60.167.20.192:1133
60.168.206.165:1133
114.98.114.43:3256
118.117.189.228:3256
60.168.81.158:1133
123.171.42.75:3256
206.81.0.107:80
118.117.188.74:3256
118.117.189.237:3256
60.168.80.97:1133
125.141.117.12:80
60.166.75.160:8888
60.168.81.177:1133
104.129.198.248:8800
178.209.51.218:5836
113.238.142.208:3128
60.168.206.104:8888
104.129.202.98:8800
104.129.206.79:8800
117.65.1.249:3256
104.129.206.67:8800
117.69.230.228:3256
117.35.254.27:3000
114.98.114.187:3256
104.129.198.143:8800
125.87.95.97:3256
121.232.148.193:3256
104.129.198.249:8800
118.117.189.184:3256
123.171.42.249:3256
114.98.114.91:3256
60.167.20.20:1133
123.171.42.67:3256
125.62.198.97:84
111.72.25.230:3256
103.35.135.30:84
104.129.204.49:8800
118.117.188.76:3256
117.69.230.22:3256
112.78.14.160:3128
103.14.199.153:83
117.65.1.130:3256
60.168.207.180:1133"""

to_visit_links = ["https://news.cnstock.com/news,bwkx-202110-4767453.htm"]  # start point: 10-15

count = 0
di={}
visited = set()
runing_proxy =None


while to_visit_links:  # BFS
    link = to_visit_links.pop(0)
    if link == "null": continue  # 不知道为什么有null
    headers = {"User-Agent": fc.user_agent()}
    # web scrape news
    time.sleep(2 + random.random())

    try:
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接 # https://blog.csdn.net/whatday/article/details/106960653
        r = s.get(link, headers=headers, proxies=runing_proxy, verify=False)
    except:
        print("Error 1")
        time.sleep(7 + random.random())
        runing_proxy = {'http': 'http://' + random.choices(proxies_list)[0]}
        r = s.get(link, headers=headers, proxies=runing_proxy, verify=False)

    html = r.content
    selector = etree.HTML(html)

    title = link.split("-")[1][:-2] + selector.xpath('//*[@id="pager-content"]/h1/text()')[0]

    xpath_list = selector.xpath('//div[@class="content"]/p')
    di[title] = [i.xpath('string(.)').strip() for i in xpath_list]
    di[title].append(xpath_list[0].xpath('//p/a/@href'))  # 单独加一列links放到最后一个元素里面, i.e. [text1, text2, [link1, link2]]

    # extend links
    visited.add(link)
    related_link_titles = selector.xpath(
        '//div[@class="relative-widget visible-md-block visible-lg-block"]/div[@class="bd"]/ul/li/a/text()')
    related_links = selector.xpath(
        '//div[@class="relative-widget visible-md-block visible-lg-block"]/div[@class="bd"]/ul/li/a/@href')

    related_link_loc = [i for i in range(len(related_link_titles)) if "市场新闻" in related_link_titles[i]]
    related_links = list(pd.Series(related_links).iloc[related_link_loc])  # 先pd.series化
    related_links = [i for i in related_links if i not in visited]  # 不重复访问

    to_visit_links = to_visit_links + related_links  # 添加上新的link
    to_visit_links = list(set(to_visit_links))
    to_visit_links = sorted(to_visit_links, reverse=True)  # 从最近到更之前的

    count += 1
    #     if count%30 == 0:
    print(title)
    print(len(to_visit_links))
    if len(di) > 365: break

os.chdir("E:\\！研三上\\00 讲座课ML\\")
# save & read

# with open("SHzhengquanbao.json", 'w') as f:
#     json.dump(di, f)
# with open("SHzhengquanbao.json", 'r') as f:
#     di = json.load(f)
