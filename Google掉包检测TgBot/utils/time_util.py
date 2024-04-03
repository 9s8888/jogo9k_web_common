# !/usr/bin/python
# -*- coding: utf-8 -*-
# @file     :time_util
# @time     :2024/3/4 14:37
# @author   :csx
# @desc     :
import datetime
import time
import pytz


class TimeUtils:
    @staticmethod
    def get_timestamp():
        '''
        获取当前时间
        :return:
        '''
        tz = pytz.timezone('Asia/Shanghai')
        beijing_time = datetime.datetime.now(tz)
        # 格式化时间为指定格式
        formatted_time = beijing_time.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_time

    @staticmethod
    def is_today(a):
        a = int(a / 1000)
        time_tuple = time.localtime(a)  # 把时间戳转换成时间元祖
        result = time.strftime("%Y%m%d", time_tuple)  # 把时间元祖转换成格式化好的时间
        return result == TimeUtils.today()

    @staticmethod
    def today():
        tz = pytz.timezone('Asia/Shanghai')
        beijing_time = datetime.datetime.now(tz)
        today = beijing_time.strftime('%Y%m%d')
        return today

    @staticmethod
    def is_enable_time(start_hour, end_hour):
        '''
        是否不生效时间
        :return:
        '''
        tz = pytz.timezone('Asia/Shanghai')
        now = datetime.datetime.now(tz)
        # 判断当前时间是否在交易时间范围内
        current_time = now.time()
        start_time = datetime.time(hour=start_hour, tzinfo=tz)
        end_time = datetime.time(hour=end_hour, tzinfo=tz)
        if start_time < current_time < end_time:
            return False
        return True


if __name__ == '__main__':
    print(TimeUtils.is_enable_time(13, 19))
