# Schedule bot

<p align="center">
  <img src="https://user-images.githubusercontent.com/72616425/103445702-d653a000-4c88-11eb-8f22-67ef3ed9e0eb.gif" alt="mock (4) (2) (demo)"/>
</p>

[![MIT License](https://img.shields.io/pypi/l/aiogram.svg?style=flat-square)](https://opensource.org/licenses/MIT)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiogram)
![Build](https://github.com/rdfsx/schedule_bot/actions/workflows/main.yml/badge.svg)


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
STATISTICS_TOKEN=1 #(токен с сайта chatbase.com, необязательно)

REDIS_HOST=localhost
REDIS_PORT=6379

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=пароль придумайте какой-нибудь

CARD_FOR_DONUTS="1234 5678 9112 3456" #номер карты для приема донатов
CARD_VALID_THRU_DONUTS= 11/22 #срок действия карты
ETHEREUM_DONUTS=0x0000000000000000000000000000000000000000 #Ethereum-адрес для донатов
BITCOIN_DONUTS=qwertyuiopasdfghjkl1234567890zxcvbnmpoiuyt #Bitcoin-адрес для донатов
```

## Использование

Запускаем бота

```console
$ cd schedule_bot

$ sudo docker-compose up
```

Чтобы завершить работу бота, нажмите Ctrl+C в терминале.
