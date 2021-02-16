# -*- coding: utf-8 -*-
import telebot
from telebot import types
import time
import ast
from string import Template


bot = telebot.TeleBot('TOKEN')

user_dict_id_main = {} # словарь с пользователями подключенными к телеграм в формате {номер чата пользователя: номер предприятия для отслеживания}
user_dict_time = {}    # словарь с пользователями которым уже была рассылка, нужен для единоразового оповещения по каждому событию

k = 0 # глобальная переменная с № чата пользователя, нужна в случае срабатывания exсept, т.к. если пытаться отослать сообщение пользователю который удалил чат с ботом, то будет сыпаться ошибка

with open('db.txt', "r") as file:
    time_dict = ast.literal_eval(file.readline())


# если /help, /start
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('/Инфо')
        itembtn2 = types.KeyboardButton('/Начать')
        markup.add(itembtn1, itembtn2)

        bot.send_message(message.chat.id, "Здравствуйте "
                         + message.from_user.first_name
                         + ", выберите кнопку <b>'/Инфо'</b> - для подробной информации, либо <b>'/Начать'</b> где необходимо указать №клана для отслеживания нападений на предприятия", reply_markup=markup, parse_mode='html')

    except Exception as e:
        bot.reply_to(message, 'Упс...!!, Error 1')


# /Инфо
@bot.message_handler(commands=['Инфо'])
def send_about(message):
    try:
        bot.send_message(message.chat.id,
                         "Привет! Это тестовый бот для игры 'Герои войны и денег' *v.0.1* \n"
                         "Доступные функции:\n"
                         "1) *Изменить клан* - можете изменить клан для отслеживания \n"
                         "2) ❌ *Выход* - выйти в начало меню\n"
                         "Если есть предложения по улучшению бота, то пишите на почту: \n"
                         "_heroeswm.telegram.bot@gmail.com_ \n"
                         "Сайт: https://www.heroeswm-telegram-bot.ru", parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, 'Упс...!!, Error 2')


# /Начать
@bot.message_handler(commands=["Начать"])
def user_reg(message):
    try:
        markup = types.ReplyKeyboardRemove(selective=False)
        msg = bot.send_message(message.chat.id, '🛡 Введите номер своего клана:', reply_markup=markup)
        bot.register_next_step_handler(msg, process_clan_step)
    except Exception as e:
        bot.reply_to(message, 'Упс...!!, Error 3')


def process_clan_step(message):

    if message.text.isdigit():
        if len(message.text) <= 5:
            chat_id = message.chat.id
            user_dict_id_main[chat_id] = message.text
            bot_button(message)
        else:
            bot.send_message(message.from_user.id, 'Нет такого клана, повторите попытку...')
            user_reg(message)
    else:
        bot.send_message(message.from_user.id, 'Номер клана должен состоять из цифр')
        user_reg(message)


def bot_button(message):
    global user_dict_id_main, k, user_dict_time

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item3 = types.KeyboardButton('Изменить клан')
    item4 = types.KeyboardButton("❌ Выход")

    markup.add(item3, item4)

    if str(len(user_dict_id_main) % 10) in '1':
        temp_heroes = str(len(user_dict_id_main)) + ' герой'

    elif str(len(user_dict_id_main) % 10) in '2, 3, 4':
        temp_heroes = str(len(user_dict_id_main)) + ' героя'

    elif str(len(user_dict_id_main) % 10) in '0, 5, 6, 7, 8, 9':
        temp_heroes = str(len(user_dict_id_main)) + ' героев'
    else:
        temp_heroes = str(len(user_dict_id_main)) + ' герой'

    bot.send_message(message.chat.id,
                     "Сейчас <b>%s</b> в сети. Поехали..." % temp_heroes.format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

    user_dict_id_main.update({message.chat.id: message.text})

    if len(user_dict_id_main) == 1: # бесконечный цикл на отслеживание запуститься только один раз, при подключении первого пользователя
        while True:
            with open('db.txt', "r") as file:
                time_dict = ast.literal_eval(file.readline())

            user_dict_id = user_dict_id_main.copy()

            try:
                for u in user_dict_id: # пробегаемся по всем пользователям которые подключены к боту
                    k = u
                    if user_dict_id[u] in time_dict:
                        if u not in user_dict_time:
                            user_dict_time[u] = time_dict[user_dict_id[u]]

                            for i in range(len(user_dict_time[u])):
                                b = list(user_dict_time[u][i].values())
                                if b == [0]:
                                    print(*user_dict_time[u][i].keys(), 'vs Сурвилурги')
                                    bot.send_message(u, str(*user_dict_time[u][i].keys()) + ' vs Сурвилурги')

                                else:
                                    count_attack = len(*user_dict_time[u][i].values())
                                    if count_attack == 1:
                                        print(*user_dict_time[u][i].keys(), 'vs', '#%s' % str(user_dict_time[u][i].values()).split("'")[1])
                                        bot.send_message(u, str(*user_dict_time[u][i].keys()) + ' vs ' + '⚔*#%s*' % str(user_dict_time[u][i].values()).split("'")[1], parse_mode='Markdown')
                                    if count_attack == 2:
                                        print(*user_dict_time[u][i].keys(), 'vs', '#%s #%s' % (str(user_dict_time[u][i].values()).split("'")[1], str(user_dict_time[u][i].values()).split("'")[3]))
                                        bot.send_message(u, str(*user_dict_time[u][i].keys()) + ' vs ' + '⚔*#%s* ⚔*#%s*' % (str(user_dict_time[u][i].values()).split("'")[1], str(user_dict_time[u][i].values()).split("'")[3]), parse_mode='Markdown')
                                    if count_attack == 3:
                                        print(*user_dict_time[u][i].keys(), 'vs', '#%s #%s #%s' % (str(user_dict_time[u][i].values()).split("'")[1], str(user_dict_time[u][i].values()).split("'")[3], str(user_dict_time[u][i].values()).split("'")[5]))
                                        bot.send_message(u, str(*user_dict_time[u][i].keys()) + ' vs ' + '⚔*#%s* ⚔*#%s* ⚔*#%s*' % (str(user_dict_time[u][i].values()).split("'")[1], str(user_dict_time[u][i].values()).split("'")[3], str(user_dict_time[u][i].values()).split("'")[5]), parse_mode='Markdown')

                        elif user_dict_time[u] == time_dict[user_dict_id[u]]:
                            # time.sleep(5)
                            continue

                        elif user_dict_time[u] != time_dict[user_dict_id[u]]:
                            for i in range(len(time_dict[user_dict_id[u]])):
                                if time_dict[user_dict_id[u]][i] not in user_dict_time[u]:
                                    b = list(time_dict[user_dict_id[u]][i].values())
                                    if b == [0]:
                                        print(*time_dict[user_dict_id[u]][i].keys(), 'vs Сурвилурги')
                                        bot.send_message(u, str(*time_dict[user_dict_id[u]][i].keys()) + ' vs Сурвилурги')

                                    else:
                                        count_attack = len(*time_dict[user_dict_id[u]][i].values())
                                        if count_attack == 1:
                                            print(*time_dict[user_dict_id[u]][i].keys(), 'vs',
                                                  '#%s' % str(time_dict[user_dict_id[u]][i].values()).split("'")[1])
                                            bot.send_message(u, str(*time_dict[user_dict_id[u]][i].keys()) + ' vs ' + '⚔*#%s*' %
                                                             str(time_dict[user_dict_id[u]][i].values()).split("'")[1],
                                                             parse_mode='Markdown')
                                        if count_attack == 2:
                                            print(*time_dict[user_dict_id[u]][i].keys(), 'vs', '#%s #%s' % (
                                            str(time_dict[user_dict_id[u]][i].values()).split("'")[1],
                                            str(time_dict[user_dict_id[u]][i].values()).split("'")[3]))
                                            bot.send_message(u, str(
                                                *time_dict[user_dict_id[u]][i].keys()) + ' vs ' + '⚔*#%s* ⚔*#%s*' % (
                                                             str(time_dict[user_dict_id[u]][i].values()).split("'")[1],
                                                             str(time_dict[user_dict_id[u]][i].values()).split("'")[3]),
                                                             parse_mode='Markdown')
                                        if count_attack == 3:
                                            print(*time_dict[user_dict_id[u]][i].keys(), 'vs', '#%s #%s #%s' % (
                                            str(time_dict[user_dict_id[u]][i].values()).split("'")[1],
                                            str(time_dict[user_dict_id[u]][i].values()).split("'")[3],
                                            str(time_dict[user_dict_id[u]][i].values()).split("'")[5]))
                                            bot.send_message(u, str(
                                                *time_dict[user_dict_id[u]][i].keys()) + ' vs ' + '⚔*#%s* ⚔*#%s* ⚔*#%s*' % (
                                                             str(time_dict[user_dict_id[u]][i].values()).split("'")[1],
                                                             str(time_dict[user_dict_id[u]][i].values()).split("'")[3],
                                                             str(time_dict[user_dict_id[u]][i].values()).split("'")[5]),
                                                             parse_mode='Markdown')

                            user_dict_time[u] = time_dict[user_dict_id[u]]
                time.sleep(5)

            except RuntimeError:
                print('RuntimeError')

            except telebot.apihelper.ApiException as e:
                if e.result.status_code == 403 or e.result.status_code == 400:
                    del user_dict_id[k]
                    del user_dict_time[k]


@bot.message_handler(content_types=['text'])
def content(message):

    if message.text == 'Изменить клан':
        if message.chat.id not in user_dict_id_main:
            process_clan_step(message)
        else:
            del user_dict_id_main[message.chat.id]
            process_clan_step(message)

    elif message.text == '❌ Выход':
        if message.chat.id not in user_dict_id_main:
            send_welcome(message)
        else:
            del user_dict_id_main[message.chat.id]
            send_welcome(message)
    else:
        bot.send_message(message.from_user.id, "Я еще не знаю такой команды ☹. Введите /help")


bot.polling(none_stop=True)