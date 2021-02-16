# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time

try:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11) AppleWebKit/514.36 (KHTML, like Gecko) Chrome/79.0.2803.116',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'keep-alive',
        'Accept-Language': 'ru-RU,ru;q=0.5,en-US;q=0.5,en;q=0.3'
    }

    your_login = 'login'
    your_password = 'password'

    s = requests.Session()
    data_login = {
        'LOGIN_redirect': '1',
        'login': your_login.encode('windows-1251'),
        'lreseted': '1',
        'pass': your_password.encode('windows-1251'),
        'preseted': '1',
        'pliv': '15000',
        'x': '1',
        'y': '1'
    }

    s.post('https://www.heroeswm.ru/login.php', data=data_login, headers=HEADERS)

    time_dict = {}

    with open('db.txt', "r") as file:
        x = file.readline()

    while True:

        try:
            time_dict = {}
            deff_requests = s.get('https://www.heroeswm.ru/mapwars.php', headers=HEADERS)
            deff_requests.encoding = 'windows-1251'

            soup_deff = BeautifulSoup(deff_requests.text, "html.parser").findAll('td', class_='wb')

            for i in range(len(soup_deff)):
                if '<i>Сурвилурги</i>' in str(soup_deff[i]):
                    clan = str(soup_deff[i]).split('<b>')[1].split('</b>')[0].split()[0][1:]
                    time_deff = str(soup_deff[i - 1]).split(':')[0][-2:] + ':' + str(soup_deff[i - 1]).split(':')[1][:2]
                    if clan not in time_dict:
                        if '<i>Сурвилурги</i> vs' in str(soup_deff[i]):
                            time_dict[clan] = [{time_deff: 0}]
                        elif '<i>Сурвилурги</i> <a' in str(soup_deff[i]):
                            list_clan = []
                            count_clan = str(soup_deff[i]).split('> vs <')[0].split('alt="#')
                            for j in range(1, len(count_clan)):
                                list_clan.append(count_clan[j].split('"')[0])
                            time_dict[clan] = [{time_deff: list_clan}]
                    elif clan in time_dict:
                        if '<i>Сурвилурги</i> vs' in str(soup_deff[i]):
                            time_dict[clan].append({time_deff: 0})
                        elif '<i>Сурвилурги</i> <a' in str(soup_deff[i]):
                            list_clan = []
                            count_clan = str(soup_deff[i]).split('> vs <')[0].split('alt="#')
                            for j in range(1, len(count_clan)):
                                list_clan.append(count_clan[j].split('"')[0])
                            time_dict[clan].append({time_deff: list_clan})

                elif '</b>Сурвилурги</i>' in str(soup_deff[i]):
                    clan = str(soup_deff[i]).split('<b>')[2].split('</b>')[0].split()[0][1:]
                    time_deff = str(soup_deff[i - 1]).split(':')[0][-2:] + ':' + str(soup_deff[i - 1]).split(':')[1][:2]
                    if clan not in time_dict:
                        if 'Сурвилурги</i> vs' in str(soup_deff[i]):
                            time_dict[clan] = [{time_deff: 0}]
                        elif 'Сурвилурги</i> <a' in str(soup_deff[i]):
                            list_clan = []
                            count_clan = str(soup_deff[i]).split('> vs <')[0].split('alt="#')
                            for j in range(1, len(count_clan)):
                                list_clan.append(count_clan[j].split('"')[0])
                            time_dict[clan] = [{time_deff: list_clan}]
                    elif clan in time_dict:
                        if 'Сурвилурги</i> vs' in str(soup_deff[i]):
                            time_dict[clan].append({time_deff: 0})
                        elif 'Сурвилурги</i> <a' in str(soup_deff[i]):
                            list_clan = []
                            count_clan = str(soup_deff[i]).split('> vs <')[0].split('alt="#')
                            for j in range(1, len(count_clan)):
                                list_clan.append(count_clan[j].split('"')[0])
                            time_dict[clan].append({time_deff: list_clan})

            if str(time_dict) != x:
                time_dict = {}
                deff_requests = s.get('https://www.heroeswm.ru/mapwars.php', headers=HEADERS)
                deff_requests.encoding = 'windows-1251'

                soup_deff = BeautifulSoup(deff_requests.text, "html.parser").findAll('td', class_='wb')

                for i in range(len(soup_deff)):
                    if '<i>Сурвилурги</i>' in str(soup_deff[i]):
                        clan = str(soup_deff[i]).split('<b>')[1].split('</b>')[0].split()[0][1:]
                        time_deff = str(soup_deff[i - 1]).split(':')[0][-2:] + ':' + str(soup_deff[i - 1]).split(':')[1][:2]
                        if clan not in time_dict:
                            if '<i>Сурвилурги</i> vs' in str(soup_deff[i]):
                                time_dict[clan] = [{time_deff: 0}]
                            elif '<i>Сурвилурги</i> <a' in str(soup_deff[i]):
                                list_clan = []
                                count_clan = str(soup_deff[i]).split('> vs <')[0].split('alt="#')
                                for j in range(1, len(count_clan)):
                                    list_clan.append(count_clan[j].split('"')[0])
                                time_dict[clan] = [{time_deff: list_clan}]
                        elif clan in time_dict:
                            if '<i>Сурвилурги</i> vs' in str(soup_deff[i]):
                                time_dict[clan].append({time_deff: 0})
                            elif '<i>Сурвилурги</i> <a' in str(soup_deff[i]):
                                list_clan = []
                                count_clan = str(soup_deff[i]).split('> vs <')[0].split('alt="#')
                                for j in range(1, len(count_clan)):
                                    list_clan.append(count_clan[j].split('"')[0])
                                time_dict[clan].append({time_deff: list_clan})

                    elif '</b>Сурвилурги</i>' in str(soup_deff[i]):
                        clan = str(soup_deff[i]).split('<b>')[2].split('</b>')[0].split()[0][1:]
                        time_deff = str(soup_deff[i - 1]).split(':')[0][-2:] + ':' + str(soup_deff[i - 1]).split(':')[1][:2]
                        if clan not in time_dict:
                            if 'Сурвилурги</i> vs' in str(soup_deff[i]):
                                time_dict[clan] = [{time_deff: 0}]
                            elif 'Сурвилурги</i> <a' in str(soup_deff[i]):
                                list_clan = []
                                count_clan = str(soup_deff[i]).split('> vs <')[0].split('alt="#')
                                for j in range(1, len(count_clan)):
                                    list_clan.append(count_clan[j].split('"')[0])
                                time_dict[clan] = [{time_deff: list_clan}]
                        elif clan in time_dict:
                            if 'Сурвилурги</i> vs' in str(soup_deff[i]):
                                time_dict[clan].append({time_deff: 0})
                            elif 'Сурвилурги</i> <a' in str(soup_deff[i]):
                                list_clan = []
                                count_clan = str(soup_deff[i]).split('> vs <')[0].split('alt="#')
                                for j in range(1, len(count_clan)):
                                    list_clan.append(count_clan[j].split('"')[0])
                                time_dict[clan].append({time_deff: list_clan})

                with open('db.txt', "w") as file:
                    file.write(str(time_dict))

            with open('db.txt', "r") as file:
                x = file.readline()

            time.sleep(5)

        except requests.ConnectionError:
            print('Ошибка соединения while')

except requests.ConnectionError:
    print('Ошибка соединения header')

