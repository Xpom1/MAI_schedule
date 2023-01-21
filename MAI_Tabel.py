import requests
import hashlib
import datetime
import pandas as pd
import difflib
from Work_With_db import get_dz_form_homework
from datetime import date
import string
import threading
import time
import os
import json


def check_file_update():
    arr = os.listdir('data')
    write_to_logs_and_print('Start Update', datetime.datetime.now().time())
    try:
        for i in arr:
            req = requests.get(f'https://public.mai.ru/schedule/data/{i}').json()
            with open(f'data/{i}', encoding='utf-8') as file:
                one, two = len(file.read()), len(str(req))
            if one != two:
                with open(f'data/{i}', 'w+', encoding='utf-8') as file:
                    json.dump(req, file, ensure_ascii=False)
                    write_to_logs_and_print('Change', i)
            time.sleep(5)
        write_to_logs_and_print('End Update', datetime.datetime.now().time())
    except requests.exceptions.ConnectTimeout:
        write_to_logs_and_print(requests.exceptions.ConnectTimeout, datetime.datetime.now().time())


def update():
    while True:
        time.sleep(21_600)
        check_file_update()


threading.Thread(target=update, daemon=True).start()

nnnedel = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']


def get_json_group_from_data(group):
    group_ = hashlib.md5(f'{group}'.encode()).hexdigest()
    try:
        with open(f"data/{group_}.json") as file:
            return json.loads(file.read())
    except FileNotFoundError:
        req = requests.get(f'https://public.mai.ru/schedule/data/{group_}.json').json()
        with open(f"data/{group_}.json", 'w+') as file:
            json.dump(req, file, ensure_ascii=False)
        with open(f"data/{group_}.json") as file:
            return json.loads(file.read())


def get_group_from_data():
    try:
        with open(f"data/groups.json") as file:
            return json.loads(file.read())
    except FileNotFoundError:
        req = requests.get(f'https://public.mai.ru/schedule/data/groups.json').json()
        with open(f"data/groups.json", 'w+') as file:
            json.dump(req, file, ensure_ascii=False)
        with open(f"data/groups.json") as file:
            return json.loads(file.read())


def rasp(group, day):
    req = get_json_group_from_data(group)
    if isinstance(day, list):
        raspisanie = list()
        raspisanie.append('-' * 30)
        raspisanie.append('')
        for days_ in day:
            try:
                kogda = req.get(f'{days_}')

                raspisanie.append(f"📆 {kogda.get('day')} ~ {'.'.join(days_.split('.')[:2])}\n")

                time_ = list(kogda.get('pairs').keys())
                homework = get_dz_form_homework(days_, group)
                for i in time_:
                    perem = kogda.get('pairs').get(i)
                    predmet = list(perem.keys())[0]
                    time_start = ':'.join(perem.get(list(perem.keys())[0]).get('time_start').split(':')[:2])
                    time_end = ':'.join(perem.get(list(perem.keys())[0]).get('time_end').split(':')[:2])
                    type_ = list(perem.get(list(perem.keys())[0]).get('type').keys())[0]
                    room = list(perem.get(list(perem.keys())[0]).get('room').values())[0]
                    lector = list(perem.get(list(perem.keys())[0]).get('lector').values())[0]
                    if lector == '':
                        raspisanie.append(f'👨🏼‍🏫 _{predmet}_\n{time_start} - {time_end}   {type_}   {room}\n')
                    else:
                        raspisanie.append(
                            f'👨🏼‍🏫 _{predmet}_\n{lector}\n{time_start} - {time_end}   {type_}   {room}\n')
                    type_predmet = f'{type_} {predmet[:22]}'
                    if type_predmet in list(homework.keys()):
                        dz = '\n'.join(homework.get(type_predmet))
                        raspisanie.append(f"📚 Дз: {dz}\n")
            except:
                raspisanie.append(f"📆 {nnnedel[day.index(days_)]} ~ {'.'.join(days_.split('.')[:2])}")
                raspisanie.append('Выходной\n')
            raspisanie.append('-' * 30)
            raspisanie.append('')
        return raspisanie
    else:
        raspisanie = []
        try:
            kogda = req.get(f'{day}')

            raspisanie.append(f"📆 {kogda.get('day')} ~ {'.'.join(day.split('.')[:2])}\n")

            time_ = list(kogda.get('pairs').keys())
            homework = get_dz_form_homework(day, group)
            for i in time_:
                perem = kogda.get('pairs').get(i)
                predmet = list(perem.keys())[0]
                time_start = ':'.join(perem.get(list(perem.keys())[0]).get('time_start').split(':')[:2])
                time_end = ':'.join(perem.get(list(perem.keys())[0]).get('time_end').split(':')[:2])
                type_ = list(perem.get(list(perem.keys())[0]).get('type').keys())[0]
                room = list(perem.get(list(perem.keys())[0]).get('room').values())[0]
                lector = list(perem.get(list(perem.keys())[0]).get('lector').values())[0]
                if lector == '':
                    raspisanie.append(f'👨🏼‍🏫 _{predmet}_\n{time_start} - {time_end}   {type_}   {room}\n')
                else:
                    raspisanie.append(f'👨🏼‍🏫 _{predmet}_\n{lector}\n{time_start} - {time_end}   {type_}   {room}\n')
                type_predmet = f'{type_} {predmet[:22]}'
                if type_predmet in list(homework.keys()):
                    dz = '\n'.join(homework.get(type_predmet))
                    raspisanie.append(f"📚 Дз: {dz}\n")
        except:
            week_ = []
            pn = datetime.date.today() + datetime.timedelta(days=-datetime.date.today().weekday())
            for i in range(0, 7):
                d = pn + datetime.timedelta(days=i)
                week_.append(d.strftime("%d.%m.%Y"))
            raspisanie.append(f"📆 {nnnedel[week_.index(day)]} ~ {'.'.join(day.split('.')[:2])}")
            raspisanie.append('Выходной')
        return raspisanie


def nonetD(date):
    return datetime.date.today().strftime("%d.%m") == date


def nonetM(date):
    return (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d.%m") == date


def lesson_day(group_, day):
    try:
        req = get_json_group_from_data(group_)
        kogda = req.get(f'{day}').get('pairs')
        times = kogda.keys()
        lesson = []
        for i in times:
            da = kogda.get(i)
            a = list(da.keys())[0].strip()
            type_ = list(da.get(a).get('type').keys())[0]
            lesson.append(f'{type_} {a}')
    except:
        lesson = []
    return lesson


def today(group_):
    today_ = datetime.date.today()
    today_ = today_.strftime("%d.%m.%Y")
    return '\n'.join(rasp(group_, today_))


def today_datetime():
    return datetime.date.today()


def tomorrow(group_):
    today_ = datetime.date.today()
    tomorrow_ = today_ + datetime.timedelta(days=1)
    tomorrow_ = tomorrow_.strftime("%d.%m.%Y")
    return '\n'.join(rasp(group_, tomorrow_))


def week(group_):
    week_ = []
    pn = datetime.date.today() + datetime.timedelta(days=-datetime.date.today().weekday())
    for i in range(0, 6):
        d = pn + datetime.timedelta(days=i)
        week_.append(d.strftime("%d.%m.%Y"))
    return '\n'.join(rasp(group_, week_))


def next_week(group_):
    next_week_ = []
    next_pn = datetime.date.today() + datetime.timedelta(days=-datetime.date.today().weekday() + 7)
    for i in range(0, 6):
        d = next_pn + datetime.timedelta(days=i)
        next_week_.append(d.strftime("%d.%m.%Y"))
    return '\n'.join(rasp(group_, next_week_))


def choose_week(group, plus_day=7):
    req = get_json_group_from_data(group)
    week_preview = {}
    for i in list(req.keys())[1:]:
        day = pd.to_datetime(f'{i}', format='%d.%m.%Y')
        if day.date() > datetime.date.today() + datetime.timedelta(days=plus_day):
            week_ = []
            pn = day + datetime.timedelta(days=-day.weekday())
            for j in range(0, 6):
                d = pn + datetime.timedelta(days=j)
                week_.append(d.strftime("%d.%m.%Y"))
            week_preview[f'{week_[0][:5]}-{week_[-1][:5]}'] = week_
    return week_preview


def may_be(find):
    req = get_group_from_data()
    group = []
    for i in req:
        group.append(i.get('name'))
    if find in group:
        return [find], 1
    else:
        otv = difflib.get_close_matches(find, group, cutoff=.8)
        if len(otv) > 0:
            return otv, 0
        else:
            return otv, -1


def mat(slova):
    return set(j.lower().translate(str.maketrans('', '', string.punctuation)) for j in slova.split()).intersection(
        set(i.get('word') for i in json.load(open('need/cenz.json')))) != set()


def write_to_logs_and_print(*args):
    text = ' '.join(list(map(str, args)))
    with open('need/logs.txt', 'a') as f:
        f.write(f'{text}\n')
    print(text)


def get_future_day(days: list) -> list:
    days_ = []
    for i in days:
        day = int(i.split('.')[0])
        month = int(i.split('.')[1])
        year = int(i.split('.')[2])
        date_ = date(year, month, day)
        today_ = datetime.date.today()
        if date_ >= today_:
            days_.append(date_.strftime("%d.%m.%Y"))
    return days_

# group = 'М6О-108Б-22'
# # Разбить все по разным файлам и бота сделать через очередь!!!
# # Мниеожно сделать сообщение, которе меняет расписание само с помощью кнопочек под сообщем
# (Захотел это оставить, тк эти строчки были с самой первой версии проекта)
# print('\n'.join(rasp(group, week)))
