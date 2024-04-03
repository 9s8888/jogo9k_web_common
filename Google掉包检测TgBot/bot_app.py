# !/usr/bin/python
# -*- coding: utf-8 -*-
# @file     :bot_app
# @time     :2024/3/4 15:17
# @author   :csx
# @desc     :
from apscheduler.schedulers.background import BackgroundScheduler
import telebot
from utils.play_util import GooglePlayUtil

bot = telebot.TeleBot("6853464189:AAH6Q6PBcehBcNsvf0OOSW_HcrksEt7zx40")


@bot.message_handler(commands=['help', 'chatid'])
def send_welcome(message):
    if message.text.lower().startswith('/chatid'):
        bot.reply_to(message, "chatid: " + str(message.chat.id))
    elif message.text.lower().startswith('/help'):
        bot.reply_to(message, "使用方法：\n1.发送 /chatid 获取chatid\n2.发送 /help 获取帮助")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


scheduler_sync = BackgroundScheduler()
scheduler_sync.add_job(GooglePlayUtil.notify_pkg_status, 'interval', minutes=3, args=[bot])
scheduler_sync.start()
scheduler_sync2 = BackgroundScheduler()
scheduler_sync2.add_job(GooglePlayUtil.confuse_url, 'interval', minutes=5)
scheduler_sync2.start()
GooglePlayUtil.notify_pkg_status(bot)
bot.infinity_polling()
