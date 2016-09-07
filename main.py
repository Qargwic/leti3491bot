#!/usr/bin/python
# -*- coding: utf-8 -*-

import telebot
import constants
import info

bot = telebot.TeleBot(constants.token)
# bot.send_message(message.from_user.id, "Дима невероятно умен и крут")


def schedule(index):
    str = ''
    i = 0
    for p in info.queue[index]:
        if p != -1:
            str = str + '<b>' + info.timeStr[i] + '</b>' + ': ' + info.clas[info.subToClas[p]] +\
                  ' | ' + info.namesOfSub[p] + \
                  '\n (' + info.teacher[info.subToTeacher[p]] + ')\n'
        i = i + 1
    if str == '':
        return 'Выходной:)'
    return str


def get_less(time, this):
    index = get_day(time)
    # print(time)
    time = get_time(time)
    # print(time)
    i = 0
    if this:
        for el in info.time:
            if el < time < (el + info.lenOfSub) and info.queue[index][i] != -1:
                return 'Текущая пара:\n' + '<b>' + info.timeStr[i] + '</b> ' + info.clas[info.subToClas[i]] + ' | ' + \
                       info.namesOfSub[info.queue[index][i]] + '\n'
            i = i + 1
        return ''
    else:
        while True:
            for el in info.time:
                if time < el and info.queue[index][i] != -1:
                    return 'Ближайшая пара:\n' + '<b>' + info.timeStr[i] + '</b> ' +\
                           info.clas[info.subToClas[info.queue[index][i]]] +\
                           ' | ' + info.namesOfSub[info.queue[index][i]]
                i = i + 1
            i = 0
            time = 0
            index = index + 1
            if index == 14:
                index = 0


def get_day(time):
    time = (time - constants.startTime) // 86400 % 14  # // Кол-во секунд в сутках % Кол-во дней
    return time


def get_time(time):
    time = (time - constants.startTime) % 86400 // 60  # % Кол-во секунд в сутках // Кол-во сек в мин
    return time + 3 * 60 * 60


@bot.message_handler(commands=['start'])
def handler_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Ближайшая пара')
    user_markup.row('Расписание на сегодня')
    user_markup.row('Расписание на завтра')
    bot.send_message(message.from_user.id, 'Добро пожаловать..', reply_markup=user_markup)


@bot.message_handler(commands=['help'])
def handler_help(message):
    bot.send_message(message.from_user.id, 'Здесь вы можете узнать расписание пар на ближайшее время')


@bot.message_handler(content_types=['text'])
def handler_text(message):
    hide_markup = telebot.types.ReplyKeyboardMarkup()
    time = message.date
    if message.text == u'Расписание на сегодня':
        bot.send_message(message.from_user.id, schedule(get_day(time)), parse_mode='HTML', reply_markup=hide_markup)
    elif message.text == u'Расписание на завтра':
        bot.send_message(message.from_user.id, schedule(get_day(time) + 1), parse_mode='HTML', reply_markup=hide_markup)
    elif message.text == u'Ближайшая пара':
        bot.send_message(message.from_user.id, get_less(time, True) + get_less(time, False),
                         parse_mode='HTML', reply_markup=hide_markup)


bot.polling(none_stop=True, interval=0)
