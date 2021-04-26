#获取城市酒店列表，保存为hotel.xlsx,之后整理转化为hotel.csv
import csv
import json
import logging
import random
import time
from concurrent.futures import ThreadPoolExecutor
import requests
from openpyxl import load_workbook
import urllib3
urllib3.disable_warnings()

def get_ip_list(filename):
    ip_list = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            ip_list.append(line.strip('\n'))
    return ip_list


def get_proxies(ip_list):
    ip = random.choice(ip_list)
    # 代理服务器
    proxyHost = ip.split(":")[0]
    proxyPort = ip.split(":")[1]
    proxyMeta = "http://%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta
    }
    return proxies

cityId = 62 #目标城市id
pageCount = 56 #最大页数
filename = '/code/data\hotelList.xlsx'
ipfile = 'G:\PythonFIle\meituan\data\ipList.txt' #代理服务器列表存放文件
title = ['id', 'year', 'city', 'name', 'brandId', 'addr', 'star', 'price', 'scoreIntro', 'comments', 'lng', 'lat',
         'count','cityId']

wb = load_workbook(filename)
sheet = wb['Sheet']
sheet.append(title)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
url = "https://ihotel.meituan.com/hbsearch/HotelSearch"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36",
    "Referer": "https://hotel.meituan.com/beijing"
}

def hotel_data(x):
    data = {
        'utm_medium': 'pc',
        'version_name': 999.9,
        'cateId': 20,
        'attr_28': 129,
        'uuid': '148E5E533C30EE4E474C84F1D580BA182639D74FB94A1C4B8658499422FD2D72@1614657653207',
        'cityId': cityId,
        'offset': x * 20,
        'limit': 20,
        'startDay': 20210303,
        'endDay': 20210304,
        'q': '', 'sort': 'defaults',
        'X-FOR-WITH': 'cqCp5+zfglIWhhyLxRkA6E8xEZfM6lWwcABK68ZSmRJuFTxUHYgs3jf0ABMUuunTtg2AKZTU87TYH0YW4PgN9sXruGLIriU2oDsZpc2IyMovpBe/tEHodqX9ud2iBKt9LrSFNHVGXWT3XJsQxbYqaQpFOHP2bSaZ4i2liuEcfTjuBPdNdk08ONVfQGrB/n1ZKC4BXNyLS4dExYWYD5jwEA=='
    }
    proxies = get_proxies(get_ip_list(ipfile))
    print(x,proxies)
    try:
        res = requests.get(url, headers=headers, params=data,proxies=proxies)
        results = json.loads(res.text)['data']['searchresult']
        print(x, ':success')
        for con in results:
            city = con['cityName']
            year = con['forward']['poiExtendsInfosDesc'][1]
            id = con['poiid']
            count = con['historyCouponCount']
            name = con['name']
            brandId = con['brandId']
            addr = con['addr']  # 酒店地址
            star = con['hotelStar']  # 酒店类型
            price = con['lowestPrice']  # 最低价
            scoreIntro = con['scoreIntro']  # 评价
            comments = con['commentsCountDesc']  # 评论数
            lng, lat = con['lng'], con['lat']  # 经纬度
            cid = cityId
            data = [id, year, city, name, brandId, addr, star, price, scoreIntro, comments, lng, lat, count,cid]
            sheet.append(data)
            logging.info(data)
            wb.save(filename)
    except requests.ConnectionError as e:
        print(e.args)
    time.sleep(random.randint(1, 4))


if __name__ == '__main__':
    page = [i for i in range(pageCount)]
    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(hotel_data, page)
