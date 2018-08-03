#-*- coding:utf-8 -*-

import time
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

from com.utils.PostGreSQL import PostGreSQL
from com.model.Weather import Weather


w_all_time = ["201101", "201102", "201103", "201104", "201105", "201106", "201107", "201108", "201109", "201110", "201111",
         "201112",
         "201201", "201202", "201203", "201204", "201205", "201206", "201207", "201208", "201209", "201210", "201211",
         "201212",
         "201301", "201302", "201303", "201304", "201305", "201306", "201307", "201308", "201309", "201310", "201311",
         "201312",
         "201401", "201402", "201403", "201404", "201405", "201406", "201407", "201408", "201409", "201410", "201411",
         "201412",
         "201501", "201502", "201503", "201504", "201505", "201506", "201507", "201508", "201509", "201510", "201511",
         "201512",
         "201601", "201602", "201603", "201604", "201605", "201606", "201607", "201608", "201609", "201610", "201611",
         "201612",
         "201701", "201702", "201703", "201704", "201705", "201706", "201707", "201708", "201709", "201710", "201711",
         "201712",
         "201801", "201802", "201803", "201804", "201805", "201806"]


#检测市县区有哪些时间的天气
def check_time(city_en, city_cn):
    url = "http://lishi.tianqi.com/{}/index.html".format(city_en)
    data_list = []
    r = s.get(url, headers={'Connection': 'close'})

    if r.url == url:
        soup = BeautifulSoup(r.text, 'html.parser')

        try:
            # 验证中文名是否对应
            box_hd_div = soup.select('div[class="box-hd"]')[0]
            hd_txt = box_hd_div.select("h3")[0].text.encode('utf-8')

            if hd_txt.find(city_cn) != -1:
                tqtongji1_div = soup.select('div[class="tqtongji1"]')[0]
                uls = tqtongji1_div.select("ul")
                for ul in uls:
                    li_times = ul.select("li")
                    for li_time in li_times:
                        data_list.append(filter(str.isdigit, li_time.string.encode('utf-8')))
        except Exception as err:
            print err
        else:
            return data_list
    return data_list


def get_weather(city_en, city_cn, w_time):
    url = "http://lishi.tianqi.com/{}/{}.html".format(city_en, w_time)
    data_list = []
    try:
        r = s.get(url, headers={'Connection': 'close'})
        soup = BeautifulSoup(r.text, 'html.parser')
        #验证中文名是否对应
        box_hd_div = soup.select('div[class="box-hd"]')[0]
        hd_txt = box_hd_div.select("h3")[0].string.encode('utf-8')

        if hd_txt.find(city_cn) != -1:
            weather_div = soup.select('div[class="tqtongji2"]')[0]
            ul_list = weather_div.select('ul')
            for ul in ul_list:
                li_list = ul.select('li')

                w_time = ''
                w_max_temperature = ''
                w_min_temperature = ''
                w_weather = ''
                w_wind_direction = ''
                w_wind_power = ''
                if not (li_list[0].string is None):
                    w_time = li_list[0].string.encode('utf-8')
                if not (li_list[1].string is None):
                    w_max_temperature = li_list[1].string.encode('utf-8')
                if not (li_list[2].string is None):
                    w_min_temperature = li_list[2].string.encode('utf-8')
                if not (li_list[3].string is None):
                    w_weather = li_list[3].string.encode('utf-8')
                if not (li_list[4].string is None):
                    w_wind_direction = li_list[4].string.encode('utf-8')
                if not (li_list[5].string is None):
                    w_wind_power = li_list[5].string.encode('utf-8')

                data = Weather(w_time, w_max_temperature, w_min_temperature, w_weather, w_wind_direction, w_wind_power)
                data_list.append(data)
            data_list.remove(data_list[0])
            s.close()
    except Exception as err:
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("%s%s%s爬取数据失败---%s\n%s" % (city_en, city_cn, w_time, time_now, err))

        print("Connection refused by the server..")
        print("Let me sleep for 5 seconds")
        print("ZZzzzz...")
        time.sleep(5)
        return get_weather(city_en, city_cn, w_time)
    else:
        return data_list

'''
if __name__ == '__main__':
    s = requests.session()
    s.keep_alive = False
    s.mount('http://', HTTPAdapter(max_retries=100))

    pgsql = PostGreSQL()
    print("所有市县区加载中..."),
    citys = pgsql.ExecQuery("select * from china_city where province_cn='广东';")
    print("\t 完毕\n开始爬取天气...")
    w_sum = 0
    for city in citys:
        weather_times = check_time(city[1].rstrip(), city[2].rstrip())
        for weather_time in weather_times:
            weathers = get_weather(city[1].rstrip(), city[2].rstrip(), weather_time)
            if weathers.__len__() != 0:
                for weather in weathers:
                    flag = pgsql.ExceNonQuery(
                        sql="insert into tianqi values("
                            "nextval('tianqi_seq'::regclass),'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'"
                            ");"
                            %
                            (
                                weather.time,
                                weather.maxTemperature,
                                weather.minTemperature,
                                weather.weather,
                                weather.windDirection,
                                weather.windPower,
                                city[0].rstrip(),
                                city[1].rstrip(),
                                city[2].rstrip(),
                                city[7].rstrip()
                            )
                        )
                    if flag is True:
                        print("info:%s添加1条天气" % city[2].rstrip())
                        w_sum = w_sum + 1
    print("执行完毕 共爬取%s条天气数据" % w_sum)
'''

#测试
s = requests.session()
s.keep_alive = False
s.mount('http://', HTTPAdapter(max_retries=100))

url = "http://lishi.tianqi.com/xingning/index.html"
r = s.get(url, headers={'Connection': 'close'})
weather_times = check_time('xingning', 'xingning')
for weather_time in weather_times:
    print weather_time
