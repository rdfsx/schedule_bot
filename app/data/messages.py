from app import config

base_message = """
Возможно, ты хотел найти расписание группы или рейтинг преподавателя, но ввёл несуществующее название.

В любом случае, это сообщение попадет администратору, и он ответит, если захочет.

/donuts - задонатить

/prepods - рейтинг и расписание преподавателей

/search - расписание чужой группы

/calls - расписание звонков

/reset или /start - сброс настроек
"""

hello_message = """
Приветствую в боте!
Исходный код доступен на github https://github.com/rdfsx/schedule_bot

Задонатить - /donuts
"""

donuts = """
Здесь можно скинуть денежку на оплату сервера или на кофе:3

<code>{card}</code>
<code>{card_date}</code>

Bitcoin:
<code>{bitcoin}</code>

Ethereum:
<code>{ethereum}</code>
""".format(card=config.CARD_FOR_DONUTS.replace('"', ''), card_date=config.CARD_VALID_THRU_DONUTS,
           bitcoin=config.BITCOIN_DONUTS, ethereum=config.ETHEREUM_DONUTS)
