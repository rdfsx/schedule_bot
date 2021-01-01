# Schedule bot

Бот-помощник для студента, который показывает расписание занятий, а также имеет систему рейтинга преподавателей.

## Installation

Для начала, нужно [создать бота с помощью Botfather](https://core.telegram.org/bots#3-how-do-i-create-a-bot)

Через Botfather разрешаем боту использовать инлайн-режим: выбираем бота, Bot Settings, Inline Mode, Turn inline mode on

### Установка 

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
