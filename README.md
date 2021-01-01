# Schedule bot

[![MIT License](https://img.shields.io/pypi/l/aiogram.svg?style=flat-square)](https://opensource.org/licenses/MIT)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiogram)


Бот-помощник для студента, который показывает расписание занятий, а также имеет систему рейтинга преподавателей.

## Структура репозитория 
```
├── app.py
├── config.py
├── Dockerfile
├── install_docker.sh
├── LICENSE
├── loader.py
├── README.md
├── requirements.txt
├── docker-compose.yml
├── data
|   ├── __init__.py
│   ├── convert.py
│   └── messages.py
├── filters
│   ├── __init__.py
│   ├── is_admin.py
│   ├── is_day.py
│   ├── is_group.py
│   └── is_teacher.py
├── handlers
│   ├── admins
│   │   ├── admin.py
│   │   └── __init__.py
│   ├── errors
│   │   ├── error_handler.py
│   │   └── __init__.py
│   ├── __init__.py
│   └── users
│       ├── commands.py
│       ├── __init__.py
│       ├── inline_handlers.py
│       ├── message_handlers.py
│       └── start.py
├── keyboards
│   ├── default
│   │   ├── __init__.py
│   │   └── menu.py
│   ├── __init__.py
│   └── inline
│       ├── callback_datas.py
│       ├── __init__.py
│       └── inline_buttons.py
├── middlewares
│   ├── acl.py
│   ├── chatbaser.py
│   ├── __init__.py
│   └── throttling.py
├── models
│   ├── fuckult.py
│   ├── __init__.py
│   ├── lessons.py
│   └── week.py
├── states
│   ├── __init__.py
│   ├── admin_state.py
│   └── user_state.py
└── utils
    ├── __init__.py
    ├── set_bot_commands.py
    ├── notify_admins.py
    ├── admin_tools
    │   ├── broadcast.py
    │   └── __init__.py
    ├── db_api
    │   ├── db_gino.py
    │   ├── __init__.py
    │   ├── commands
    │   │   ├── commands_teacher.py
    │   │   ├── commands_timetable.py
    │   │   ├── commands_user.py
    │   │   ├── coomands_group.py
    │   │   └── __init__.py
    │   └── schemas
    │       ├── group.py
    │       ├── __init__.py
    │       ├── schedule.py
    │       ├── teacher.py
    │       └── user.py
    ├── misc
    │   ├── __init__.py
    │   ├── logger.py
    │   └── throttling.py
    ├── redis
    │   ├── consts.py
    │   └── __init__.py
    └── stats
        ├── chatbase.py
        └── __init__.py
```
## Установка

Для начала, нужно [создать бота с помощью Botfather](https://core.telegram.org/bots#3-how-do-i-create-a-bot)

Через Botfather разрешаем боту использовать инлайн-режим: выбираем бота, Bot Settings, Inline Mode, Turn inline mode on

### Ubuntu

1. Установим git, если он ещё не установлен

```bash
$ sudo apt install git -y
```

2. Установим docker-compose

```bash
$ sudo apt install docker-compose -y
```

3. Склонируем репозиторий бота

```bash
$ git clone https://github.com/rdfsx/schedule_bot.git
```

4. Переходим в папку с ботом

```bash
$ cd schedule_bot
```

5. Создаём файл .env, куда пропишем данные для запуска, в том числе токен бота из Botfather

```
$ nano .env
```
Прописываем:
```
ADMIN_ID=ваш id в telegram
BOT_TOKEN=токен бота
STATISTICS_TOKEN=1 (токен с сайта chatbase.com, необязательно)
ip=db
redis_ip=redis
PGUSER=postgres
PGPASSWORD=пароль придумайте какой-нибудь

DATABASE=postgres
```

## Использование

Запускаем бота

```bash
$ cd schedule_bot

$ sudo docker-compose up
```

Чтобы завершить работу бота, нажмите Ctrl+C в терминале.
