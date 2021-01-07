# Schedule bot

<p align="center">
  <img src="https://user-images.githubusercontent.com/72616425/103445702-d653a000-4c88-11eb-8f22-67ef3ed9e0eb.gif" alt="mock (4) (2) (demo)"/>
</p>

[![MIT License](https://img.shields.io/pypi/l/aiogram.svg?style=flat-square)](https://opensource.org/licenses/MIT)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiogram)


Бот-помощник для студента, который показывает расписание занятий, а также имеет систему рейтинга преподавателей.

## Установка

Для начала, нужно [создать бота с помощью Botfather](https://core.telegram.org/bots#3-how-do-i-create-a-bot)

Через Botfather разрешаем боту использовать инлайн-режим: выбираем бота, Bot Settings, Inline Mode, Turn inline mode on

### Ubuntu

1. Установим git, если он ещё не установлен

```console
$ sudo apt install git -y
```

2. Установим docker-compose

```console
$ sudo apt install docker-compose -y
```

3. Склонируем репозиторий бота

```console
$ git clone https://github.com/rdfsx/schedule_bot.git
```

4. Переходим в папку с ботом

```console
$ cd schedule_bot
```

5. Создаём файл .env, куда пропишем данные для запуска, в том числе токен бота из Botfather

```console
$ nano .env
```
Прописываем:
```
ADMIN_ID=ваш id в telegram
BOT_TOKEN=токен бота
STATISTICS_TOKEN=1 (токен с сайта chatbase.com, необязательно)

REDIS_HOST=localhost
REDIS_PORT=6379

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=пароль придумайте какой-нибудь
```

## Использование

Запускаем бота

```console
$ cd schedule_bot

$ sudo docker-compose up
```

Чтобы завершить работу бота, нажмите Ctrl+C в терминале.

## Структура репозитория 
```

├── app.py                                                 # Тут запускаем бота
├── config.py                                              # Подтягиваем данные для работы бота из .env
├── Dockerfile
├── install_docker.sh
├── LICENSE
├── loader.py                                              # Инициализация бота, базы данных, машины состояний и т.д. 
├── README.md
├── requirements.txt                                       # Зависимости
├── docker-compose.yml
|
├── data
|   ├── __init__.py
│   ├── convert.py
│   └── messages.py
|
├── filters                                                # Фильтры для обработчиков сообщений
│   ├── __init__.py
│   ├── is_admin.py
│   ├── is_day.py
│   ├── is_group.py
│   └── is_teacher.py
|
├── handlers                                               # Хэндлеры (обработчики)
│   ├── __init__.py
|   |
│   ├── admins                                             # Только сообщения администратора
│   │   ├── admin.py
│   │   └── __init__.py
|   |
│   ├── errors                                             # Обработка исключений
│   │   ├── error_handler.py
│   │   └── __init__.py
|   |
│   └── users                                              # Сообщения от пользователя
|       ├── __init__.py
│       ├── commands.py                                    # Обработка команд
│       ├── inline_handlers.py                             # Инлайн-запросы
│       ├── message_handlers.py                            # Текстовые сообщения (кроме комманд)
│       └── start.py                                       # Регистрация пользователя
|
├── keyboards                                              # Кнопки (инлайн и обычные)
│   ├── __init__.py
|   |
│   ├── default
│   │   ├── __init__.py
│   │   └── menu.py
|   |
│   └── inline
│       ├── __init__.py
│       ├── callback_datas.py                              # Создание callback-data (информация, которая передаётся при нажатии на инлайн-кнопку)
│       └── inline_buttons.py                              
|
├── middlewares                                            # Мидлвари (обработка апдейта перед хэндлером)
│   ├── __init__.py
│   ├── acl.py
│   ├── chatbaser.py                                       # Отправка статистики на сервис chatbase.com
│   └── throttling.py                                      # Троттлинг (ограничение количества отправляемых пользователем запросов)
|
├── models                                                 # Классы enum
│   ├── __init__.py
│   ├── fuckult.py
│   ├── lessons.py
│   └── week.py
|
├── states                                                 # Состояния для машины состояний (FSM)
│   ├── __init__.py
│   ├── admin_state.py
│   └── user_state.py
|
└── utils                                                  # Утилиты
    ├── __init__.py
    ├── set_bot_commands.py                                # Установка комманд для бота,
    ├── notify_admins.py                                   # Оповещения администраторов
    |
    ├── admin_tools
    │   ├── broadcast.py                                   # Рассылка сообщения по пользователям
    │   └── __init__.py
    |
    ├── db_api                                             # Работа с базой данных
    │   ├── __init__.py
    │   ├── db_gino.py                                     # Подключение к базе данных
    |   |
    │   ├── commands                                       # Работа с таблицами
    │   │   ├── commands_teacher.py
    │   │   ├── commands_timetable.py
    │   │   ├── commands_user.py
    │   │   ├── coomands_group.py
    │   │   └── __init__.py
    |   |
    │   └── schemas                                        # Схемы таблиц
    │       ├── __init__.py
    │       ├── group.py
    │       ├── schedule.py
    │       ├── teacher.py
    │       └── user.py
    |
    ├── misc
    │   ├── __init__.py
    │   ├── logger.py                                      # Логгирование
    │   └── throttling.py
    |
    ├── redis                                              # Работа с базой данных redis для хранения состояний
    │   ├── consts.py
    │   └── __init__.py
    |
    └── stats                                              # Работа с chatbase.com
        ├── chatbase.py
        └── __init__.py
```
