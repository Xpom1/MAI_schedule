from MAI_Tabel import *
from Work_With_db import *
from Token import token, myid
import logging
import datetime

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())


def rate_limit(limit: int):
    def decorator(func):
        setattr(func, "throttling_rate_limit", limit)
        return func

    return decorator


def get_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text="Сегодня", callback_data="day_today"),
        types.InlineKeyboardButton(text="Завтра", callback_data="day_tomorrow"),
        types.InlineKeyboardButton(text="Неделя", callback_data="day_week"),
        types.InlineKeyboardButton(text="Сл. Неделя", callback_data="day_nextweek"),
        types.InlineKeyboardButton(text="Выбр. Недели", callback_data="day_Newweek"),
        types.InlineKeyboardButton(text="Добав. Дз", callback_data="DZ_add"),
        types.InlineKeyboardButton(text="Инфо", callback_data="day_info"),
        types.InlineKeyboardButton(text="Новая группа", callback_data="day_newgroup")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_today() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text="*Сегодня*", callback_data="day_Nonetd"),
        types.InlineKeyboardButton(text="Завтра", callback_data="day_tomorrow"),
        types.InlineKeyboardButton(text="Неделя", callback_data="day_week"),
        types.InlineKeyboardButton(text="Сл. Неделя", callback_data="day_nextweek"),
        types.InlineKeyboardButton(text="Выбр. Недели", callback_data="day_Newweek"),
        types.InlineKeyboardButton(text="Добав. Дз", callback_data="DZ_add"),
        types.InlineKeyboardButton(text="Инфо", callback_data="day_info"),
        types.InlineKeyboardButton(text="Новая группа", callback_data="day_newgroup")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_tomorrow() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text="Сегодня", callback_data="day_today"),
        types.InlineKeyboardButton(text="*Завтра*", callback_data="day_Nonetm"),
        types.InlineKeyboardButton(text="Неделя", callback_data="day_week"),
        types.InlineKeyboardButton(text="Сл. Неделя", callback_data="day_nextweek"),
        types.InlineKeyboardButton(text="Выбр. Недели", callback_data="day_Newweek"),
        types.InlineKeyboardButton(text="Добав. Дз", callback_data="DZ_add"),
        types.InlineKeyboardButton(text="Инфо", callback_data="day_info"),
        types.InlineKeyboardButton(text="Новая группа", callback_data="day_newgroup")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_week() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text="Сегодня", callback_data="day_today"),
        types.InlineKeyboardButton(text="Завтра", callback_data="day_tomorrow"),
        types.InlineKeyboardButton(text="*Неделя*", callback_data="day_None"),
        types.InlineKeyboardButton(text="Сл. Неделя", callback_data="day_nextweek"),
        types.InlineKeyboardButton(text="Выбр. Недели", callback_data="day_Newweek"),
        types.InlineKeyboardButton(text="Добав. Дз", callback_data="DZ_add"),
        types.InlineKeyboardButton(text="Инфо", callback_data="day_info"),
        types.InlineKeyboardButton(text="Новая группа", callback_data="day_newgroup")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_nextweek() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text="Сегодня", callback_data="day_today"),
        types.InlineKeyboardButton(text="Завтра", callback_data="day_tomorrow"),
        types.InlineKeyboardButton(text="Неделя", callback_data="day_week"),
        types.InlineKeyboardButton(text="*Сл. Неделя*", callback_data="day_None"),
        types.InlineKeyboardButton(text="Выбр. Недели", callback_data="day_Newweek"),
        types.InlineKeyboardButton(text="Добав. Дз", callback_data="DZ_add"),
        types.InlineKeyboardButton(text="Инфо", callback_data="day_info"),
        types.InlineKeyboardButton(text="Новая группа", callback_data="day_newgroup")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_info() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text="Сегодня", callback_data="day_today"),
        types.InlineKeyboardButton(text="Завтра", callback_data="day_tomorrow"),
        types.InlineKeyboardButton(text="Неделя", callback_data="day_week"),
        types.InlineKeyboardButton(text="Сл. Неделя", callback_data="day_nextweek"),
        types.InlineKeyboardButton(text="Выбр. Недели", callback_data="day_Newweek"),
        types.InlineKeyboardButton(text="Добав. Дз", callback_data="DZ_add"),
        types.InlineKeyboardButton(text="*Инфо*", callback_data="day_None"),
        types.InlineKeyboardButton(text="Новая группа", callback_data="day_newgroup")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


def gen_markup(weeks) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i in range(len(weeks)):
        markup.insert(types.InlineKeyboardButton(f"{list(weeks.keys())[i]}",
                                                 callback_data=f"weeks_{list(weeks.keys())[i]}"))
    markup.insert(types.InlineKeyboardButton(f"Назад", callback_data=f"DZ_back"))
    return markup


def gen_week_dz(weeks) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i in range(len(weeks)):
        markup.insert(types.InlineKeyboardButton(f"{list(weeks.keys())[i]}",
                                                 callback_data=f"DZ_weeks_{list(weeks.keys())[i]}"))
    markup.insert(types.InlineKeyboardButton(f"Назад", callback_data=f"DZ_back"))
    return markup


def gen_dz_answer() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(f"Нет", callback_data=f"answerdz_No"),
        types.InlineKeyboardButton(f"Поменять Дз", callback_data=f"answerdz_change"),
        types.InlineKeyboardButton(f"Да", callback_data=f"answerdz_Yes")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


def gen_back() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.insert(types.InlineKeyboardButton(f"Назад", callback_data=f"DZ_back"))
    return markup


def gen_day_dz(days) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    days_ = get_future_day(days)
    for i in range(len(days_)):
        markup.insert(types.InlineKeyboardButton(f"{days_[i]}",
                                                 callback_data=f"DZ_days_{days_[i]}"))
    markup.insert(types.InlineKeyboardButton(f"В начало", callback_data=f"DZ_add"))
    return markup


def gen_lesson_dz(group, day) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    lesson = lesson_day(group, day)
    if len(lesson) > 0:
        for i in range(len(lesson)):
            markup.insert(types.InlineKeyboardButton(f"{lesson[i][:25]}...",
                                                     callback_data=f"DZ_lesson_{lesson[i][:25]}"))
        markup.insert(types.InlineKeyboardButton(f"В начало", callback_data=f"DZ_add"))
    else:
        markup.insert(types.InlineKeyboardButton(f"В начало", callback_data=f"DZ_add"))
    return markup


def gen_group_(group) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.insert(types.InlineKeyboardButton(f"Нет", callback_data=f"gr_No"))
    markup.insert(types.InlineKeyboardButton(f"Да", callback_data=f"gr_{group}"))
    return markup


def gen_group_2(group) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.insert(types.InlineKeyboardButton(f"Нет", callback_data=f"gr2_No"))
    markup.insert(types.InlineKeyboardButton(f"Да", callback_data=f"gr2_{group}"))
    return markup


class UserState(StatesGroup):
    group = State()
    change_gr = State()
    dz = State()


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    await message.answer("Привет! Это расписание МАИ ✈"
                         "\nМожете воспользоваться командой:"
                         "\n/timetable - Расписание")


@dp.message_handler(commands='changegroup')
async def change_group(message: types.Message):
    user_id = message.chat.id
    info = get_info_about_user_id_whitelist(user_id)
    if info is not None:
        wait = update_homework_group_days(user_id)
        if wait > 0:
            await message.answer(f'До смены группы вам осталось {wait} дней')
            await message.answer("Расписание на:", reply_markup=get_keyboard())
        else:
            await message.answer(
                'Теперь вам доступна функция смены группы.'
                '\nУкажите номер новой учебной группы,'
                '\nдля которой хотите записывать домашнее задание.'
                '\nПример: М6О-108Б-22')
            await UserState.change_gr.set()
    else:
        await message.answer(f'Для выполнения этой команды вы должны'
                             f'\nбыть зарегистрированы. Для этого нажмите Добав. Дз')
        await message.answer("Расписание на:", reply_markup=get_keyboard())


@dp.message_handler(state=UserState.change_gr)
async def get_group(message: types.Message, state: FSMContext):
    await state.update_data(change_gr=message.text)
    may, ch = may_be(message.text)
    date_ = datetime.datetime.today().date()
    if ch == 1:
        user = message.chat.id
        text = message.text
        write_to_logs_and_print(datetime.datetime.now(), user, text, 'new group wl')
        update_group_wl(user, text, date_)
        await message.answer("Расписание на:", reply_markup=get_keyboard())
        await state.finish()
    elif ch == 0:
        keyboard = gen_group_2(may[0])
        await message.answer(f"Можеть быть {may[0]} ?", reply_markup=keyboard)
        await state.finish()
    else:
        await message.answer("Вы указали некоректную группу!\nПопробуйте еще раз")
        await state.finish()
        await UserState.change_gr.set()


@dp.message_handler(commands='delbl')
async def del_bl(message: types.Message):
    if message.chat.id == myid:
        user_id = message.get_args()
        try:
            delit_user_from_blacklist(user_id)
            await message.answer('Good')
        except:
            await message.answer('Id not in BL')


@dp.message_handler(commands='stats')
async def del_bl(message: types.Message):
    if message.chat.id == myid:
        with open('need/logs.txt') as f:
            logs = ''.join(f.readlines()[::-1][:15][::-1])
        wl, bl = number_of_wl_and_bl()
        await message.answer(f'Total users: {number_of_people()}'
                             f'\nWhitelist: {wl}'
                             f'\nBlacklist: {bl}'
                             f'\nHomework`s: {number_of_homework()}'
                             f'\n'
                             f'\nLast log:'
                             f'\n{logs}')


@dp.message_handler(commands='reg')
async def send_reg(message: types.Message):
    id_ = message.chat.id
    info_wl = get_info_about_user_id_whitelist(id_)
    info_bl = get_info_about_user_id_blacklist(id_)
    group_ = get_group_in_people(id_)

    if info_wl is None and info_bl is None:
        kb = [
            [
                types.KeyboardButton('Отправить свой контакт ☎', request_contact=True)
            ],
        ]
        markup_request = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(f'Вы будете записывать домашнее задание для {group_}. 👽'
                             '\nЕсли Вы хотите поменять группу, то воспользуйтесь командой /timetable'
                             '\n'
                             '\nУсловия пользования:'
                             '\n•Запрещается загружать информацию'
                             '\n не относящуюся к домашнему заданию.'
                             '\n•Запрещается спамить.'
                             '\n•Запрещается использование нецензурной лексики.'
                             '\n'
                             '\nЗа несоблюдение вышеперечисленных правил'
                             '\nпредусматривается блокировка пользователя.'
                             '\n'
                             '\n★Функция смены группы для записи'
                             '\n домашнего задания доступна 1 раз в месяц.'
                             '\n'
                             '\nНажимая на кнопку «Отправить свой контакт»'
                             '\nВы соглашаетесь с условиями пользования.',
                             reply_markup=markup_request)
    elif info_wl is not None and info_bl is None:
        await message.answer('Вы уже зарегистрированы')
        await message.answer("Расписание на:", reply_markup=get_keyboard())
    elif info_wl is None and info_bl is not None:
        await message.answer('Вы внесены в черный список!', reply_markup=gen_back())


@dp.message_handler(content_types=['contact'])
async def contact(message: types.Message):
    if message.contact is not None:
        id_ = message.chat.id
        group_ = get_group_in_people(id_)
        add_writer(dict_=message.contact.to_python(), group=group_, date_=datetime.datetime.now().date())
        await message.answer(text=f'Готово 👍'
                                  f'\nТеперь Вы можете добавлять домашнее задание,'
                                  f'\nкоторое будет доступно каждому студенту,'
                                  f'\nсостоящему в группе {group_}'
                                  f'\nДля того чтобы поменять группу, воспользуйтесь командой /changegroup',
                             reply_markup=types.ReplyKeyboardRemove())
        await message.delete()
        await message.answer("Расписание на:", reply_markup=get_keyboard())


@dp.message_handler(commands='timetable')
async def timetable(message: types.Message):
    await message.answer("Напишите свою группу:\nПример: М6О-108Б-22")
    await UserState.group.set()


@dp.message_handler(state=UserState.dz)
async def get_dz_writter(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    colvo = 256
    if len(message.text) <= colvo:
        await message.delete()
        dz_ = '\n'.join(list(filter(None, message.text.split('\n'))))
        update_dz(user_id, dz_)
        group, date_, lesson, dz, delmsg = get_info_about_dz(user_id)
        try:
            await bot.delete_message(user_id, message_id=delmsg)
        except Exception as err:
            write_to_logs_and_print(err)

        await message.answer(
            f'Вы хотите записать Дз\n Для: {group}\n На: {date_}\n Предмет: {lesson[:20]}...\n Дз: {dz}',
            reply_markup=gen_dz_answer(), parse_mode='Markdown')
        await state.finish()
    else:
        msg = await message.answer(f"Вы превысили лимит по символам. "
                                   f"\nПожалуйста, сократите ваш текст до {colvo} знаков."
                                   f"\nНапишите ДЗ:")
        update_delmsg(user_id, msg.message_id)
        await state.finish()
        await UserState.dz.set()


@dp.message_handler(state=UserState.group)
async def get_group(message: types.Message, state: FSMContext):
    await state.update_data(group=message.text)
    may, ch = may_be(message.text)
    if ch == 1:
        user = message.chat.id
        text = message.text
        write_to_logs_and_print(datetime.datetime.now(), user, text)
        write_groupe_to_people(user, text)
        await message.answer("Расписание на:", reply_markup=get_keyboard())
    elif ch == 0:
        keyboard = gen_group_(may[0])
        await message.answer(f"Можеть быть {may[0]} ?", reply_markup=keyboard)
    else:
        await message.answer("Вы указали некоректную группу!\nНажмите - /timetable")
    await state.finish()


@rate_limit(limit=5)
@dp.callback_query_handler(Text(startswith="day_"))
async def callbacks(call):
    with suppress(MessageNotModified):
        group = get_group_in_people(call.message.chat.id)
        action = call.data.split("_")[1]
        write_to_logs_and_print(datetime.datetime.now(), call.message.chat.id, group, action)
        if action == "today":
            await call.message.edit_text(f"{today(group)}", reply_markup=get_keyboard_today(), parse_mode='Markdown')
        elif action == "tomorrow":
            await call.message.edit_text(f"{tomorrow(group)}", reply_markup=get_keyboard_tomorrow(),
                                         parse_mode='Markdown')
        elif action == "week":
            await call.message.edit_text(f"{week(group)}", reply_markup=get_keyboard_week(), parse_mode='Markdown')
        elif action == "nextweek":
            await call.message.edit_text(f"{next_week(group)}", reply_markup=get_keyboard_nextweek(),
                                         parse_mode='Markdown')
        elif action == "Newweek":
            weeks_ = choose_week(group)
            markup = gen_markup(weeks_)
            await call.message.edit_text("Выберите неделю:", reply_markup=markup)
        elif action == "info":
            id_ = call.message.chat.id
            gr_wl = get_group_wl(id_)
            await call.message.edit_text(
                f'Вы смотрите расписание для группы {group}'
                f'\nВы записываете расписание для {gr_wl}'
                f'\n'
                f'\n/timetable - Поменять группу просмотра дз'
                f'\n/changegroup - Поменять группу для записи дз'
                f"\n"
                f"\nAuthor: Xpom 😶‍🌫️"
                f"\nNews: [*Новости проекта*](https://t.me/MAI_bot_news)"
                f"\nSuggestion: [*Предложения и пожелания*]"
                f"(https://docs.google.com/forms/d/17FaSjvEWHyFMZTsL4dCXefbz_oWdfQnkk8xCz2wZl6U)"
                f"\nGithub: [*Другие проекты автора*](https://github.com/Xpom1)"
                f"\nTg: [*Контакты*](https://t.me/Xpom7)",
                reply_markup=get_keyboard_info(), parse_mode='Markdown', disable_web_page_preview=True)
        elif action == "newgroup":
            await call.message.edit_text("Напишите свою группу:")
            await UserState.group.set()
        elif 'None' in action:
            try:
                date_ = call.message.text.split('\n')[0].split('~')[1].strip()
            except IndexError:
                date_ = '00.00'
            if action == 'Nonetd' and not nonetD(date_) or action == 'Nonetm' and not nonetM(date_):
                if action == 'Nonetd':
                    await call.message.edit_text(f"{today(group)}", reply_markup=get_keyboard_today(),
                                                 parse_mode='Markdown')
                else:
                    await call.message.edit_text(f"{tomorrow(group)}", reply_markup=get_keyboard_tomorrow(),
                                                 parse_mode='Markdown')
            else:
                await call.answer('Уже выбрано 🙃', show_alert=True)
    await call.answer()


@rate_limit(limit=5)
@dp.callback_query_handler(Text(startswith="answerdz_"))
async def callbacks_dz(call):
    user_id = call.message.chat.id
    action = call.data.split("_")[1]
    if action == 'No':
        delete_from_temp(user_id)
        await call.message.edit_text(f"Расписание на:", reply_markup=get_keyboard(), parse_mode='Markdown')
    elif action == 'change':
        msg = await call.message.edit_text(f"Напишите ДЗ:")
        update_delmsg(user_id, msg.message_id)
        await UserState.dz.set()
    elif action == 'Yes':
        group_, date_, lesson, dz, delmsg = get_info_about_dz(user_id)
        if mat(dz):
            send_to_blacklist(user_id)
            await call.answer('Вы нарушили правила\nВы в бане!', show_alert=True)
            await call.message.edit_text(f"Расписание на:", reply_markup=get_keyboard(), parse_mode='Markdown')
        else:
            dz_ = '\n'.join(list(filter(None, dz.split('\n'))))
            bit = add_dz_to_homework(user_id, date_, group_, lesson, dz_)
            if bit == 1:
                await call.answer('Дз успешно добавлено 🔥', show_alert=True)
                await call.message.edit_text(f"Расписание на:", reply_markup=get_keyboard(), parse_mode='Markdown')
                write_to_logs_and_print(datetime.datetime.now(), user_id, date_, dz)
            elif bit == 0:
                await call.answer('На этот предмет уже записано максимальное кол-во заданий', show_alert=True)
                await call.message.edit_text(f"Расписание на:", reply_markup=get_keyboard(), parse_mode='Markdown')
        delete_from_temp(user_id)


@dp.callback_query_handler(Text(startswith="weeks_"))
async def callbacks(call):
    group = get_group_in_people(call.message.chat.id)
    action = call.data.split("_")[1]
    weeks_ = choose_week(group)
    if action in weeks_:
        text = '\n'.join(rasp(group, weeks_.get(action)))
        await call.message.edit_text(f"{text}", reply_markup=get_keyboard(), parse_mode='Markdown')
    await call.answer()


@dp.callback_query_handler(Text(startswith="gr_"))
async def callbacks(call):
    action = call.data.split("_")[1]
    if action != 'No':
        user = call.message.chat.id
        text = action
        write_to_logs_and_print(datetime.datetime.now(), user, text)
        write_groupe_to_people(user, text)
        await call.message.edit_text(f"Расписание на:", reply_markup=get_keyboard(), parse_mode='Markdown')
    else:
        await call.message.edit_text("Напишите свою группу:\nПример: М6О-108Б-22")
        await UserState.group.set()
    await call.answer()


@dp.callback_query_handler(Text(startswith="gr2_"))
async def callbacks(call):
    action = call.data.split("_")[1]
    date_ = datetime.datetime.today().date()
    if action != 'No':
        user = call.message.chat.id
        text = action
        write_to_logs_and_print(datetime.datetime.now(), user, text)
        update_group_wl(user, text, date_)
        await call.message.edit_text(f"Расписание на:", reply_markup=get_keyboard(), parse_mode='Markdown')
    else:
        await call.message.edit_text("Напишите свою группу:\nПример: М6О-108Б-22")
        await UserState.change_gr.set()
    await call.answer()


@rate_limit(limit=5)
@dp.callback_query_handler(Text(startswith="DZ_"))
async def callbacks(call):
    user_id = call.message.chat.id
    action = call.data.split("_")[1]
    group = get_group_wl(user_id)
    info_wl = get_info_about_user_id_whitelist(user_id)
    info_bl = get_info_about_user_id_blacklist(user_id)
    if action == 'add':
        if info_wl is None and info_bl is None:
            await call.message.edit_text('Для регистрации воспользуйтесь командой /reg')
        elif info_wl is not None and info_bl is None:
            weeks_ = choose_week(group, 0)
            await call.message.edit_text(f'Вы записываете домашнее задание для {group}'
                                         '\n\nВыберете неделю на которую хотите записать дз:',
                                         reply_markup=gen_week_dz(weeks_),
                                         parse_mode='Markdown')
        elif info_wl is None and info_bl is not None:
            await call.message.edit_text('Вы внесены в черный список!', reply_markup=gen_back())

    elif action == 'back':
        await call.message.edit_text(f"Расписание на:", reply_markup=get_keyboard(), parse_mode='Markdown')

    elif action == 'weeks':
        weeks_ = choose_week(group, 0)
        week_ = call.data.split("_")[2]
        days = weeks_.get(week_)
        await call.message.edit_text(f'Вы записываете домашнее задание для {group}'
                                     f"\n\nВыберете день:", reply_markup=gen_day_dz(days), parse_mode='Markdown')
    elif action == 'days':
        day = call.data.split("_")[2]
        gr_wl = get_group_wl(user_id)
        add_gr_date_temp(user_id, gr_wl, day)
        await call.message.edit_text(f"Вы записываете домашнее задание для {group}"
                                     f"\n\nВыберете предмет:", reply_markup=gen_lesson_dz(group, day),
                                     parse_mode='Markdown')
    elif action == 'lesson':
        update_lesson(user_id, call.data.split("_")[2])
        msg = await call.message.edit_text(f"Вы записываете домашнее задание для {group}"
                                           f"\n\nНапишите ДЗ:")
        update_delmsg(user_id, msg.message_id)
        await UserState.dz.set()
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
