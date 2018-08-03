#-*- coding:utf-8 -*-


class Weather(object):
    def __init__(self, time, maxTemperature, minTemperature, weather, windDirection, windPower):
        self.time = time
        self.maxTemperature = maxTemperature
        self.minTemperature = minTemperature
        self.weather = weather
        self.windDirection = windDirection
        self.windPower = windPower

    def show_info(self):
        print("日期：%s \n最高气温：%s\n最低气温：%s\n天气：%s\n风向：%s\n风力：%s" %
              (self.time,
               self.maxTemperature,
               self.minTemperature,
               self.weather,
               self.windDirection,
               self.windPower)
              )