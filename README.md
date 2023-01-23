[//]: # ([![Typing SVG]&#40;https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=Computer+science+student&#41;]&#40;https://git.io/typing-svg&#41;)

[//]: # ()
[//]: # ([![KnlnKS's LeetCode stats]&#40;https://leetcode-stats-six.vercel.app/api?username=Xpom7&theme=dark&#41;]&#40;https://leetcode.com/Xpom7/&#41;)

# Про бота :cactus:

Ссылка на [бота](https://t.me/MAI_tabel_bot)

Публикации:
[One](https://vk.com/maevnik?w=wall-58942429_119383)
[Two](https://t.me/MAIuniversity/3262)


- [Как все работает?
](https://github.com/Xpom1/MAI_schedule#%D0%BA%D0%B0%D0%BA-%D0%B2%D1%81%D0%B5-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82)
- [Статистика](https://github.com/Xpom1/MAI_schedule#%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D0%B0)
- [Асинхронность](https://github.com/Xpom1/MAI_schedule#%D0%B0%D1%81%D0%B8%D0%BD%D1%85%D1%80%D0%BE%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D1%8C)
- [Работа с DB](https://github.com/Xpom1/MAI_schedule#%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0-%D1%81-db)
- [Coroutine](https://github.com/Xpom1/MAI_schedule#coroutine)
- [Цензура](https://github.com/Xpom1/MAI_schedule#%D1%86%D0%B5%D0%BD%D0%B7%D1%83%D1%80%D0%B0)
- [Интересные решения](https://github.com/Xpom1/MAI_schedule#%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D0%B5%D1%81%D0%BD%D1%8B%D0%B5-%D1%80%D0%B5%D1%88%D0%B5%D0%BD%D0%B8%D1%8F)

___
## Как все работает? 

Для начала нужно пройти авторизацию и указать свою группу

Тут можно ошибиться пока пишешь свою группу, поэтому бот может подсказать

![](photo/img(COPY).png)

Теперь вы можете смотреть расписание на любой удобный вам день

![](photo/img_1(COPY).png)

Так же вам доступна функция добавления домашнего задания (Как это делают учителя в школах)

Но для этого нужно пройти регистрацию

![](photo/img_2(COPY).png)

После регистрации у вас в информации отобразится ваш статус, для какой группы вы можете записывать дз

![](photo/img_3(COPY).png)

Теперь вы можете записывыть дз, для этого надо нажать на кнопку "Добав. Дз" 

Выбираете неделю на которую хотите записать дз

![](photo/img_4(COPY).png)

Далее день

![](photo/img_5(COPY).png)

Выбираете предмет и записываете дз

![](photo/img_6(COPY).png)

После всего этого вам нужно подтвердить вашу запись этого дз, тк его **смогут увидеть все ваши одногруппники**

![](photo/img_7(COPY).png)

Бууууум :boom:

Теперь оно отображается для всех)

![](photo/img_8(CPOY).png)

[UP:arrow_up:](https://github.com/Xpom1/MAI_schedule#%D0%BF%D1%80%D0%BE-%D0%B1%D0%BE%D1%82%D0%B0-cactus)
___
## Статистика

Данная статистика актуальна на 23.01.2023

Общее количество пользователей: **1100+**

Уникальных запросов в день: **140+**

![](photo/img_9(CPOY).png)

Нагрузка на сервер

![](photo/img_stats.png)

[UP:arrow_up:](https://github.com/Xpom1/MAI_schedule#%D0%BF%D1%80%D0%BE-%D0%B1%D0%BE%D1%82%D0%B0-cactus)

___
## Асинхронность

Она была достигнута с помощью библиотеки [aiogram](https://docs.aiogram.dev/en/latest/)

Ознкомиться можно тут [Bot_aiogram](Bot_aiogram.py)

[UP:arrow_up:](https://github.com/Xpom1/MAI_schedule#%D0%BF%D1%80%D0%BE-%D0%B1%D0%BE%D1%82%D0%B0-cactus)

___
## Работа с DB

Была использована библиотека [**sqlite3**](https://docs.python.org/3/library/sqlite3.html)

Все основные методы реализации предоставлены в [Work_With_db](Work_With_db.py)

[UP:arrow_up:](https://github.com/Xpom1/MAI_schedule#%D0%BF%D1%80%D0%BE-%D0%B1%D0%BE%D1%82%D0%B0-cactus)

___
## Coroutine

Реализована с помощью [threading](https://docs.python.org/3/library/threading.html)
```python
def update():
    while True:
        time.sleep(21_600)
        check_file_update()

threading.Thread(target=update, daemon=True).start()
```
Этот код запускает скрипт, который каждые 6 часов обновляет данные о файлах

Нужно для хранения актуальных файлов

[UP:arrow_up:](https://github.com/Xpom1/MAI_schedule#%D0%BF%D1%80%D0%BE-%D0%B1%D0%BE%D1%82%D0%B0-cactus)

___

## Цензура
Была реалезованна проверка на маты
```python
def mat(slova):
    return set(j.lower().translate(str.maketrans('', '', string.punctuation)) for j in slova.split()).intersection(
        set(i.get('word') for i in json.load(open('need/cenz.json')))) != set()
```

[UP:arrow_up:](https://github.com/Xpom1/MAI_schedule#%D0%BF%D1%80%D0%BE-%D0%B1%D0%BE%D1%82%D0%B0-cactus)

___
## Интересные решения

С помощью этого кода была реализована задержка перед нажатиями кнопок, чтобы уменьшить нагрузку на сервер
```python
def rate_limit(limit: int):
    def decorator(func):
        setattr(func, "throttling_rate_limit", limit)
        return func
    return decorator
```

Сделан генератор клавиатуры
```python
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
```

[UP:arrow_up:](https://github.com/Xpom1/MAI_schedule#%D0%BF%D1%80%D0%BE-%D0%B1%D0%BE%D1%82%D0%B0-cactus)
