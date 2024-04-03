# !/usr/bin/python
# -*- coding: utf-8 -*-
# @file     :excel_read
# @time     :2024/3/4 13:37
# @author   :csx
# @desc     :
import time
import os
import pandas as pd
import requests
import urllib3
import traceback
import json
import random
from utils.time_util import TimeUtils

urllib3.disable_warnings()


def log(*args):
    try:
        print(f'{TimeUtils.get_timestamp()}\n', *args)
    except:
        pass


class GooglePlayUtil:
    @staticmethod
    def get_pks(index=1):
        '''
        获取需要检测的
        :return:
        '''
        config = {}
        log('获取安装包列表')
        keys = ['url', 'name', 'chat_id', 'a_name', 'nickname', 'interval', 'key_un1', 'key_un2']
        url = 'https://docs.google.com/spreadsheets/d/1g_M-IyVCuHNBZmGRH3DSudtHAYmvQsdhejQoiSb9fec/export?format=csv'
        try:
            df = pd.read_csv(url)
            columns = df.columns.tolist()
            # 将 DataFrame 转换为字典
            data_dict = df.to_dict(orient='records')
            custom_json_data = []
            for item in data_dict:
                custom_item = {}
                for idx, key in enumerate(columns):
                    value = item[key]
                    if isinstance(value, str):
                        try:
                            value = value.encode('latin1').decode('utf-8')
                        except:
                            pass
                    if pd.isna(value):
                        value = None
                    custom_item[keys[idx]] = value
                    config[keys[idx]] = key
                if custom_item['url'] and custom_item['url'].startswith('https'):
                    custom_json_data.append(custom_item)
            return custom_json_data, config
        except:
            if index > 3:
                return None, None
            else:
                index = index + 1
                return GooglePlayUtil.get_pks(index)

    @staticmethod
    def get_pkg_status(pkg_url, index=1,max=3):
        '''
        检测安装包状态
        :return:
        '''
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
        try:
            status_code = requests.get(url=pkg_url, headers=headers, verify=False,timeout=120).status_code
            return status_code == 200, True
        except:
            print(traceback.format_exc())
            if index >= max:
                return False, False
            else:
                index = index + 1
                return GooglePlayUtil.get_pkg_status(pkg_url, index,max)

    @staticmethod
    def confuse_url():
        '''
        混淆连接访问
        :return:
        '''
        pkgs, config = GooglePlayUtil.get_pks()
        if config:
            try:
                intervals = config['interval'].split('-')
                start = abs(int(intervals[0])-300)
                end = abs(int(intervals[1]))
                time.sleep(random.randint(start, end))
            except:
                time.sleep(random.randint(0, 300))
        if pkgs:
            new_pkgs = []
            for pkg in pkgs:
                if not pkg['chat_id']:
                    new_pkgs.append(pkg)
            if new_pkgs:
                pkg = random.choice(new_pkgs)
                pkg_url = pkg['url']
                log('混淆',GooglePlayUtil.get_pkg_status(pkg_url,max=(int(config['key_un2'])+1)))

    @staticmethod
    def notify_pkg_status(bot):
        '''
        通知
        :param self:
        :param bot:
        :return:
        '''
        records = {}
        if os.path.exists('record.json'):
            with open('record.json', 'r', encoding='utf-8') as f:
                txt = f.read()
                try:
                    records = json.loads(txt)
                except:
                    pass
        new_records = {}
        pkgs, config = GooglePlayUtil.get_pks()
        # c_ids = ['-4186561706','-1002134438286']
        if pkgs:
            new_pkgs = []
            for pkg in pkgs:
                if pkg['chat_id']:
                    new_pkgs.append(pkg)
            print(new_pkgs)
            for pkg in new_pkgs:
                # pkg['chat_id'] = random.choice(c_ids)
                try:
                    if pkg['interval']:
                        intervals = pkg['interval'].split('-')
                        start = int(intervals[0])
                        end = int(intervals[1])
                        if not TimeUtils.is_enable_time(start_hour=start, end_hour=end):
                            print(pkg['a_name'],'不在检测时间范围内')
                            continue
                except:
                    print(traceback.format_exc())
                status, flag = GooglePlayUtil.get_pkg_status(pkg['url'],max=(int(config['key_un2'])+1))
                if flag:
                    if not status and pkg['chat_id']:
                        # if f'{TimeUtils.today()}-{pkg["url"]}' not in records:
                        try:
                            text = f'《{TimeUtils.get_timestamp()} gp掉包预警》\n\n上架包：{pkg["a_name"]}丨{pkg["name"]}\n地址：{pkg["url"]} 疑似掉包\n请@{pkg["nickname"]}及时查看\n确认后请及时更新监测信息'
                            bot.send_message(chat_id=pkg['chat_id'], text=text)
                            new_records[f'{TimeUtils.today()}-{pkg["url"]}'] = True
                            log(text)
                        except:
                            print(traceback.format_exc())
                    elif pkg['chat_id']:
                        text = f'《{TimeUtils.get_timestamp()} gp包正常》 {pkg["name"]} 地址：{pkg["url"]}'
                        log(text)
                try:
                    time.sleep(int(config['a_name']))
                except:
                    time.sleep(60)
        try:
            with open('record.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(new_records, ensure_ascii=False, indent=4))
        except:
            print(traceback.format_exc())


if __name__ == '__main__':
    # pkgs, config = GooglePlayUtil.get_pks()
    # print(json.dumps(pkgs, ensure_ascii=False, indent=4))
    # print(json.dumps(config, ensure_ascii=False, indent=4))
    GooglePlayUtil.confuse_url()
