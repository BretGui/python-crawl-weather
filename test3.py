#-*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup


if __name__ == '__main__':
    url = 'http://lishi.tianqi.com/wuhan/201806.html'
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    weather_div = soup.select('div[class="tqtongji2"]')[0]
    ul_list = weather_div.select('ul')
    for ul in ul_list:
        li_list = ul.select('li')
        print("日期：%s\n最高气温：%s\n最低气温：%s\n天气：%s\n风向：%s\n风力：%s\n" %
              (li_list[0].string.encode('utf-8'),
               li_list[1].string.encode('utf-8'),
               li_list[2].string.encode('utf-8'),
               li_list[3].string.encode('utf-8'),
               li_list[4].string.encode('utf-8'),
               li_list[5].string.encode('utf-8'))
              )