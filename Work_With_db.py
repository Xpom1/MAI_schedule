import sqlite3
import datetime
from datetime import date

db_Homework = sqlite3.connect('db/Homework.db', check_same_thread=False)
sql_Homework = db_Homework.cursor()

sql_Homework.execute("""CREATE TABLE IF NOT EXISTS path (
    user INTEGER,
    group_ TEXT,
    date TEXT,
    lesson TEXT,
    dz TEXT,
    delmsg TEXT
)""")

sql_Homework.execute("""CREATE TABLE IF NOT EXISTS homework (
    user INTEGER,
    date TEXT,
    group_ TEXT,
    lesson TEXT,
    dz TEXT
)""")

db_Homework.commit()

db_List = sqlite3.connect('db/List.db', check_same_thread=False)
sql_List = db_List.cursor()

sql_List.execute("""CREATE TABLE IF NOT EXISTS whitelist (
    phone_number TEXT,
    first_name TEXT,
    last_name TEXT,
    user_id TEXT,
    group_ TEXT,
    date_ TEXT
)""")

sql_List.execute("""CREATE TABLE IF NOT EXISTS blacklist (
    phone_number TEXT,
    first_name TEXT,
    last_name TEXT,
    user_id TEXT,
    group_ TEXT,
    date_ TEXT
)""")

db_List.commit()

db_people = sqlite3.connect('db/people.db', check_same_thread=False)
sql_people = db_people.cursor()

sql_people.execute("""CREATE TABLE IF NOT EXISTS users (
    user INTEGER,
    group_ TEXT
)""")

db_people.commit()


def get_info_about_user_id_blacklist(user_id):
    info = sql_List.execute('SELECT * FROM blacklist WHERE user_id=?', (user_id,))
    return info.fetchone()


def send_to_blacklist(user_id):
    phone_number, first_name, last_name, group_ = 0, 0, 0, 0
    for val in sql_List.execute(
            f"SELECT phone_number, first_name, last_name, group_ FROM whitelist WHERE user_id = {user_id}"):
        phone_number = val[0]
        first_name = val[1]
        last_name = val[2]
        group_ = val[3]
    sql_List.execute(f"INSERT INTO blacklist VALUES (?, ?, ?, ?, ?, ?)",
                     (phone_number, first_name, last_name, user_id, group_, datetime.datetime.now().date()))
    sql_List.execute(f"DELETE FROM whitelist WHERE user_id = '{user_id}'")
    db_List.commit()


def get_info_about_user_id_whitelist(user_id):
    info = sql_List.execute('SELECT * FROM whitelist WHERE user_id=?', (user_id,))
    return info.fetchone()


def add_writer(dict_, group, date_):
    user_id = dict_.get('user_id')
    if get_info_about_user_id_whitelist(user_id) is None:
        phone_number = dict_.get('phone_number')
        first_name = dict_.get('first_name')
        last_name = dict_.get('last_name')
        sql_List.execute(f"INSERT INTO whitelist VALUES (?, ?, ?, ?, ?, ?)",
                         (phone_number, first_name, last_name, user_id, group, date_))
    db_List.commit()


def write_groupe_to_people(user, text):
    info = sql_people.execute('SELECT * FROM users WHERE user=?', (user,))
    if info.fetchone() is None:
        sql_people.execute(f"INSERT INTO users VALUES (?, ?)", (user, text))
    else:
        sql_people.execute(f"Update users SET group_ = '{text}' WHERE user = {user}")
    db_people.commit()


def get_group_in_people(id_):
    group = 0
    for val in sql_people.execute(f"SELECT group_ FROM users WHERE user = {id_}"):
        group = val[0].replace('_', '-')
    return group


def add_gr_date_temp(user_, group, date_):
    info = sql_Homework.execute('SELECT * FROM path WHERE user=?', (user_,))
    if info.fetchone() is None:
        dz, lesson_, delmsg = 0, 0, 0
        sql_Homework.execute(f"INSERT INTO path VALUES (?, ?, ?, ?, ?, ?)", (user_, group, date_, lesson_, dz, delmsg))
    else:
        sql_Homework.execute(f"Update path SET date = '{date_}' WHERE user = {user_}")
    db_Homework.commit()


def update_lesson(user_, lesson_):
    sql_Homework.execute(f"Update path SET lesson = '{lesson_}' WHERE user = {user_}")
    db_Homework.commit()


def update_dz(user_, dz):
    sql_Homework.execute(f"Update path SET dz = '{dz.strip()}' WHERE user = {user_}")
    db_Homework.commit()


def update_delmsg(user_, delmsg):
    sql_Homework.execute(f"Update path SET delmsg = '{delmsg}' WHERE user = {user_}")
    db_Homework.commit()


def get_info_about_dz(user_):
    group, date_, lesson, dz, delmsg = 0, 0, 0, 0, 0
    for val in sql_Homework.execute(f"SELECT group_, date, lesson, dz, delmsg FROM path WHERE user = {user_}"):
        group = (val[0]).replace('_', '-')
        date_ = val[1]
        lesson = val[2]
        dz = val[3]
        delmsg = val[4]
    return group, date_, lesson, dz, delmsg


def delete_from_temp(user_):
    sql_Homework.execute(f"DELETE FROM path WHERE user = {user_}")
    db_Homework.commit()


def add_dz_to_homework(user, date_, group_, lesson, dz) -> int:
    info_ = sql_Homework.execute('SELECT dz FROM homework WHERE date=? AND group_=? AND lesson=?',
                                 (date_, group_, lesson,)).fetchall()
    max_voluem_homework = 5
    if len(info_) < max_voluem_homework:
        info = sql_Homework.execute('SELECT * FROM homework WHERE date=? AND group_=? AND lesson=? and dz=?',
                                    (date_, group_, lesson, dz,)).fetchone()
        if info is None:
            sql_Homework.execute(f"INSERT INTO homework VALUES (?, ?, ?, ?, ?)", (user, date_, group_, lesson, dz))
            db_Homework.commit()
        return 1
    elif len(info_) == max_voluem_homework:
        return 0


def get_dz_form_homework(date_, group_) -> dict:
    homework = {}
    for val in sql_Homework.execute(f"SELECT dz, lesson FROM homework WHERE date = '{date_}' AND group_ = '{group_}'"):
        if val[1] not in homework.keys():
            homework[val[1]] = []
        homework[val[1]].append(val[0])
    return homework


def update_homework_group_days(user_id) -> int:
    date_ = sql_List.execute('SELECT date_ FROM whitelist WHERE user_id=?', (user_id,)).fetchone()[0].split('-')
    date_ = list(map(int, date_))
    date_now = list(map(int, str(datetime.datetime.today().date()).split('-')))
    d0 = date(date_[0], date_[1], date_[2])
    d1 = date(date_now[0], date_now[1], date_now[2])
    delta = (d1 - d0).days
    wait = 31 - delta
    return wait


def update_group_wl(user_id, group_, date_):
    sql_List.execute(f"Update whitelist SET group_ = '{group_}' WHERE user_id = {user_id}")
    sql_List.execute(f"Update whitelist SET date_ = '{date_}' WHERE user_id = {user_id}")
    db_List.commit()


def get_group_wl(user_id) -> str:
    group_ = 0
    for val in sql_List.execute(
            f"SELECT group_ FROM whitelist WHERE user_id = {user_id}"):
        group_ = val[0]
    if group_ != 0:
        return group_
    else:
        return '(Вам нужно пройти регистрацию)'


def delit_user_from_blacklist(user_id):
    sql_List.execute(f"DELETE FROM blacklist WHERE user_id = '{user_id}'")
    db_List.commit()


def number_of_people():
    return sql_people.execute('SELECT COUNT(*) FROM users').fetchone()[0]


def number_of_wl_and_bl():
    wl = sql_List.execute('SELECT COUNT(*) FROM whitelist').fetchone()[0]
    bl = sql_List.execute('SELECT COUNT(*) FROM blacklist').fetchone()[0]
    return wl, bl


def number_of_homework():
    return sql_Homework.execute('SELECT COUNT(*) FROM homework').fetchone()[0]
