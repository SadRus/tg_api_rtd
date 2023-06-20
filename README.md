# Tg API

Библиотека tg_api упрощает работу с веб-API Telegram. Она предоставляет тонкую обёртку над веб API Telegram и библиотекой [HTTPX](https://www.python-httpx.org/). Библиотека tg_api добавляет к HTTPX схемы данных и удобные часто используемые функции, но не мешает, при необходимости, спускаться ниже на уровень HTTP-запросов.

Ключевые возможности библиотеки tg_api:

- Поддержка синхронных и асинхронных запросов к API
- Shortcuts для часто используемых запросов
- Лёгкий доступ к боту из любого места в коде
- Наглядные схемы данных для всех типов запросов и ответов API
- Аннотация типов для удобства работы с IDE
- Простое низкоуровневое API для кастомизации запросов к API
- Набор инструментов для удобной работы с исключениями

## Ключевые концепции

Библиотека tg_api предлагает несколько необычных концепций для работы с API. Пробежимся по ним вкратце.

**No God Object**. Библиотека не предоставляет пользователю никакого аналога "god object" для работы с API, как то `TgBot` или `TgApi`. В других библиотеках часто можно увидеть подобный код:

```py
bot = TgBot(token=...)
bot.send_message(text='Hello world!', chat_id=43)
```

Такой подход прекрасно выглядит в туториалах, он кажется простым и естественным, но ему сильно не хватает гибкости. При интенсивном использовании и кастомизации вы неизбежно столкнётесь с нехваткой документации, неожиданными ограничениями ПО и вам придётся лезть в код библиотеки, чтобы решить свою проблему. Подробно типичные проблемы такого подхода описаны в антипаттерне [God object](https://ru.wikipedia.org/wiki/%D0%91%D0%BE%D0%B6%D0%B5%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9_%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82).

В библиотеке tg_api нет и не будет аналога объекта `Bot`. Вместо него для отправки запросов используются объекты `SendMessageRequest`, `SendPhotoRequest` и подобные Request-объекты, по одному для каждому API endpoint из [документации Telegram](here https://core.telegram.org/bots/api). Сначала вы готовите запрос к API, затем отправляете и обрабатываете результат. Пример:

```py
# создаём объект запроса, но ещё не отправляем
tg_request = SendMessageRequest(text='Hello world!', chat_id=43)
# отправляем запрос в API
# вызов метода поднимет исключение TgRuntimeError если сервере Telegram ответит HTTP статусом != 2xx
tg_response: SendMessageResponse = tg_request.send()
```

Преимущество такого подхода в том, что он не создаёт лишних обёрток над схемой запроса и ответа к API. Вам не нужно искать документацию по методу `send_message`, не нужно мириться с ограничениями этого метода. Вы сможете отправлять в API даже запросы с крайне нетипичными параметрами, и полная схема доступных параметров у вас всегда под рукой.

**Default configuration**. Вам не нужен прямой доступ к объекту `TgBot`, `TgApi` или `TgClient` для работы с API. Обычно приходится таскать подобный объект за собой из функции в функцию, чтобы где-то там глубоко внутри отправить пользователю сообщение в Tg. Библиотека `tg_api` использует `contextvars`, чтобы передавать настройки подключения неявно. Пример:


```py
def do_something():
    # Function send message without direct access to TgClient object
    tg_request = SendMessageRequest(text='Hello world!', chat_id=43)
    tg_request.send()


def main(token: str) -> None:
    with TgClient.setup(token):
        do_something()
```

## Примеры использования


### Синхронное API

Пример отправки пользователю текстового сообщения:

```py
from tg_api import SyncTgClient, SendMessageRequest


with SyncTgClient.setup(token):
    tg_request = SendMessageRequest(chat_id=tg_chat_id, text='Message proofs high level usage.')
    tg_request.send()
```

Пример отправки пользователю сообщения с клавиатурой:
```py
from tg_api import (
    SyncTgClient,
    SendMessageRequest,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def main(token: str, chat_id: int) -> None:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='button_1', callback_data='test'),
                InlineKeyboardButton(text='button_2', callback_data='test'),
            ],
        ],
    )
    with SyncTgClient.setup(token):
        tg_request = SendMessageRequest(
            chat_id=chat_id,
            text='Message proofs keyboard support.',
            reply_markup=keyboard,
        )
        tg_request.send()
```

### Асинхронное API

Пример отправки пользователю текстового сообщения:

```py
from tg_api import AsyncTgClient, SendMessageRequest


async with AsyncTgClient.setup(token):
    tg_request = SendMessageRequest(chat_id=chat_id, text='Message proofs high level API usage.')
    # вызов метода поднимет исключение TgRuntimeError если сервере Telegram ответит HTTP статусом != 2xx
    await tg_request.asend()
```

Пример отправки пользователю сообщения с клавиатурой:

```py
from tg_api import (
    AsyncTgClient,
    SendMessageRequest,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


async def main(token: str, chat_id: int) -> None:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='button_1', callback_data='test'),
                InlineKeyboardButton(text='button_2', callback_data='test'),
            ],
        ],
    )
    async with AsyncTgClient.setup(token):
        tg_request = SendMessageRequest(
            chat_id=chat_id,
            text='Message proofs keyboard support.',
            reply_markup=keyboard,
        )
        await tg_request.asend()
```


### Низкоуровневое API

Низкоуровневое API позволяет использовать все самые свежие возможности веб API Telegram, даже если их поддежку ещё не успели завезти
в библиотеку tg_api. Можно добавлять свои типы запросов и ответов API, менять способ отправки HTTP-запросов и реакции на ответ.

Пример использования низкоуровневого асинхронного API:

```py
from httpx import Response as HttpResponse
from tg_api import AsyncTgClient, SendMessageRequest, SendMessageResponse, raise_for_tg_response_status


async def main(token: str, chat_id: int) -> None:
    async with AsyncTgClient.setup(token) as tg_client:
        tg_request = SendMessageRequest(chat_id=chat_id, text='Message proofs low level API usage.')
        json_bytes = tg_request.json(exclude_none=True).encode('utf-8')

        http_response: HttpResponse = await tg_client.session.post(
            f'{tg_client.api_root}sendMessage',
            headers={'content-type': 'application/json'},
            content=json_bytes,
        )
        # поднимет исключение TgRuntimeError если сервере Telegram ответит HTTP статусом != 2xx
        raise_for_tg_response_status(http_response)

        tg_response = SendMessageResponse.parse_raw(http_response.content)
        print('Id нового сообщения:', tg_response.result.message_id)
```


## Документация по API

- [tg_methods.py](./tg_methods.py) -- схемы запросов к API и ответов
- [tg_types.py](./tg_methods.py) -- библиотека типов данных, с которыми работает Telegram API
