# Tg API

![PyPI - Downloads](https://img.shields.io/pypi/dm/tg_api)
![PyPI - License](https://img.shields.io/pypi/l/tg_api)

Библиотека Tg API упрощает работу с веб-API Telegram. Она предоставляет тонкую обёртку над веб API Telegram и библиотекой [HTTPX](https://www.python-httpx.org/). Библиотека Tg API добавляет к HTTPX схемы данных и удобные часто используемые функции, но не мешает, при необходимости, спускаться ниже на уровень HTTP-запросов.

Ключевые возможности библиотеки Tg API:

- Поддержка синхронных и асинхронных запросов к API
- Shortcuts для часто используемых запросов
- Лёгкий доступ к боту из любого места в коде
- Наглядные схемы данных для всех типов запросов и ответов API
- Аннотация типов для удобства работы с IDE
- Простое низкоуровневое API для кастомизации запросов к API
- Набор инструментов для удобной работы с исключениями

Документация: [https://tg-api.readthedocs.io/ru/latest/](https://tg-api.readthedocs.io/ru/latest/)

## Содержимое

1. [Ключевые концепции](#key-conceptions)
1. [Примеры использования](#usage-examples)
    1. [Синхронное API](#usage-examples-sync)
    1. [Асинхронное API](#usage-examples-async)
    1. [Низкоуровневое API](#usage-examples-low-level)

<a name="key-conceptions"></a>
## Ключевые концепции

Библиотека Tg API предлагает несколько необычных концепций для работы с API. Пробежимся по ним вкратце.

**No God Object**. Библиотека не предоставляет пользователю никакого аналога "god object" для работы с API, как то `TgBot` или `TgApi`. В других библиотеках часто можно увидеть подобный код:

```py
bot = TgBot(token=...)
bot.send_message(text='Hello world!', chat_id=43)
```

Такой подход прекрасно выглядит в туториалах, он кажется простым и естественным, но ему сильно не хватает гибкости. При интенсивном использовании и кастомизации вы неизбежно столкнётесь с нехваткой документации, неожиданными ограничениями ПО и вам придётся лезть в код библиотеки, чтобы решить свою проблему. Подробно типичные проблемы такого подхода описаны в антипаттерне [God object](https://ru.wikipedia.org/wiki/%D0%91%D0%BE%D0%B6%D0%B5%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9_%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82).

В библиотеке Tg API нет и не будет аналога объекта `Bot`. Вместо него для отправки запросов используются объекты `SendMessageRequest`, `SendPhotoRequest` и подобные Request-объекты, по одному для каждому API endpoint из [документации Telegram](here https://core.telegram.org/bots/api). Сначала вы готовите запрос к API, затем отправляете и обрабатываете результат. Пример:

```py
# создаём объект запроса, но ещё не отправляем
tg_request = SendMessageRequest(text='Hello world!', chat_id=43)
# отправляем запрос в API
# вызов метода поднимет исключение TgRuntimeError если сервере Telegram ответит HTTP статусом != 2xx
tg_response: SendMessageResponse = tg_request.send()
```

Преимущество такого подхода в том, что он не создаёт лишних обёрток над схемой запроса и ответа к API. Вам не нужно искать документацию по методу `send_message`, не нужно мириться с ограничениями этого метода. Вы сможете отправлять в API даже запросы с крайне нетипичными параметрами, и полная схема доступных параметров у вас всегда под рукой.

**Default configuration**. Вам не нужен прямой доступ к объекту `TgBot`, `TgApi` или `TgClient` для работы с API. Обычно приходится таскать подобный объект за собой из функции в функцию, чтобы где-то там глубоко внутри отправить пользователю сообщение в Tg. Библиотека `Tg API` использует `contextvars`, чтобы передавать настройки подключения неявно. Пример:


```py
def do_something():
    # Function send message without direct access to TgClient object
    tg_request = SendMessageRequest(text='Hello world!', chat_id=43)
    tg_request.send()


def main(token: str) -> None:
    with TgClient.setup(token):
        do_something()
```

<a name="usage-examples"></a>
## Примеры использования

<a name="usage-examples-sync"></a>
### Синхронное API

Пример отправки пользователю текстового сообщения:

```py
from tg_api import SyncTgClient, SendMessageRequest


with SyncTgClient.setup(token):
    tg_request = SendMessageRequest(chat_id=tg_chat_id, text='Message proofs high level usage.')
    tg_request.send()
```

Пример удаления у пользователя любого сообщения по идентификатору сообщения:

```py
from tg_api import SyncTgClient, DeleteMessageRequest


with SyncTgClient.setup(token):
    tg_request = DeleteMessageRequest(chat_id=tg_chat_id, message_id=message_id)
    tg_request.send()
```


Пример изменения у пользователя текста любого сообщения по идентификатору сообщения:

```py
from tg_api import SyncTgClient, EditMessageTextRequest


with SyncTgClient.setup(token):
    tg_request = EditMessageTextRequest(chat_id=tg_chat_id, message_id=message_id, text='edited text')
    tg_request.send()
```

Пример изменения у пользователя заголовка сообщения по идентификатору сообщения:

```py
from tg_api import SyncTgClient, EditMessageCaptionRequest


with SyncTgClient.setup(token):
    tg_request = EditMessageCaptionRequest(chat_id=chat_id, message_id=message_id, caption='edited caption')
    tg_request.send()
```

Пример изменения у пользователя фото в сообщении по URL по идентификатору сообщения:

```py
from tg_api import SyncTgClient, EditUrlMessageMediaRequest


with SyncTgClient.setup(token):
    media = InputMediaUrlDocument(
        media='https://link_to_photo.jpg',
        caption='caption'
    )
    tg_request = EditUrlMessageMediaRequest(chat_id=chat_id, message_id=message_id, media=media)
    tg_request.send()
```


Пример изменения у пользователя документа в сообщении чтением документента из файла по идентификатору сообщения:

```py
from tg_api import SyncTgClient, EditBytesMessageMediaRequest, InputMediaBytesDocument


with SyncTgClient.setup(token):
    with open('path_to_document.pdf', 'rb') as f:
        media_content = f.read()
    media = InputMediaBytesDocument(
        media='attach://attachement.pdf',
        media_content=media_content,
        caption='caption'
    )
    tg_request = EditBytesMessageMediaRequest(chat_id=chat_id, message_id=message_id, media=media)
    tg_request.send()
```


Пример изменения у пользователя клавиатуры любого сообщения по идентификатору сообщения:

```py
from tg_api import SyncTgClient, InlineKeyboardButton, InlineKeyboardMarkup


keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='button_1', callback_data='test'),
            InlineKeyboardButton(text='button_2', callback_data='test'),
        ],
    ],
)

with SyncTgClient.setup(token):
    tg_request = EditMessageReplyMarkupRequest(chat_id=tg_chat_id, message_id=message_id, reply_markup=keyboard)
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

Пример отправки пользователю фото из файловой системы:
```py
from tg_api import SyncTgClient, SendBytesPhotoRequest

def main():
    with SyncTgClient.setup(token):
        with open(photo_filename, 'rb') as f:
            photo_content = f.read()
        tg_request = SendBytesPhotoRequest(chat_id=chat_id, photo=photo_content, filename=photo_filename)
        tg_request.send()
```


Пример отправки пользователю фото по URL:
```py
from tg_api import SyncTgClient, SendUrlPhotoRequest

def main():
    with SyncTgClient.setup(token):
        tg_request = SendUrlPhotoRequest(chat_id=chat_id, photo=photo_url, filename=photo_filename)
        tg_request.send()
```

Пример отправки пользователю документа из файловой системы:
```py
from tg_api import SyncTgClient, SendBytesDocumentRequest

def main():
    with SyncTgClient.setup(token):
        with open(document_filename, 'rb') as f:
            document_content = f.read()
        tg_request = SendBytesDocumentRequest(chat_id=chat_id, document=document_content, filename=document_filename)
        tg_request.send()
```


Пример отправки пользователю документа по URL:
```py
from tg_api import SyncTgClient, SendUrlDocumentRequest

def main():
    with SyncTgClient.setup(token):
        tg_request = SendUrlDocumentRequest(chat_id=chat_id, document=document_url, filename=document_filename)
        tg_request.send()
```

<a name="usage-examples-async"></a>
### Асинхронное API

Пример отправки пользователю текстового сообщения:

```py
from tg_api import AsyncTgClient, SendMessageRequest


async with AsyncTgClient.setup(token):
    tg_request = SendMessageRequest(chat_id=chat_id, text='Message proofs high level API usage.')
    # вызов метода поднимет исключение TgRuntimeError если сервере Telegram ответит HTTP статусом != 2xx
    await tg_request.asend()
```

Пример удаления у пользователя любого сообщения по идентификатору сообщения:

```py
from tg_api import AsyncTgClient, DeleteMessageRequest


async with AsyncTgClient.setup(token):
    tg_request = DeleteMessageRequest(chat_id=chat_id, message_id=message_id)
    await tg_request.asend()
```

Пример изменения у пользователя текста любого сообщения по идентификатору сообщения:

```py
from tg_api import AsyncTgClient, EditMessageTextRequest


async with AsyncTgClient.setup(token):
    tg_request = EditMessageTextRequest(chat_id=chat_id, message_id=message_id, text='edited text')
    await tg_request.asend()
```


Пример изменения у пользователя фото в сообщении по URL по идентификатору сообщения:

```py
from tg_api import AsyncTgClient, EditUrlMessageMediaRequest


async with AsyncTgClient.setup(token):
    media = InputMediaUrlDocument(
        media='https://link_to_photo.jpg',
        caption='caption'
    )
    tg_request = EditUrlMessageMediaRequest(chat_id=chat_id, message_id=message_id, media=media)
    await tg_request.asend()
```


Пример изменения у пользователя документа в сообщении чтением документента из файла по идентификатору сообщения:

```py
from tg_api import AsyncTgClient, EditBytesMessageMediaRequest, InputMediaBytesDocument


async with AsyncTgClient.setup(token):
    with open('path_to_document.pdf', 'rb') as f:
        media_content = f.read()
    media = InputMediaBytesDocument(
        media='attach://attachement.pdf',
        media_content=media_content,
        caption='caption'
    )
    tg_request = EditBytesMessageMediaRequest(chat_id=chat_id, message_id=message_id, media=media)
    await tg_request.asend()
```


Пример изменения у пользователя клавиатуры любого сообщения по идентификатору сообщения:

```py
from tg_api import AsyncTgClient, InlineKeyboardButton, InlineKeyboardMarkup


keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='button_1', callback_data='test'),
            InlineKeyboardButton(text='button_2', callback_data='test'),
        ],
    ],
)

async with AsyncTgClient.setup(token):
    tg_request = EditMessageReplyMarkupRequest(chat_id=chat_id, message_id=message_id, reply_markup=keyboard)
    await tg_request.asend()
```

Пример изменения у пользователя заголовка сообщения по идентификатору сообщения:

```py
from tg_api import AsyncTgClient, EditMessageCaptionRequest


async with AsyncTgClient.setup(token):
    tg_request = EditMessageCaptionRequest(chat_id=chat_id, message_id=message_id, caption='edited caption')
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


Пример отправки пользователю фото из файловой системы:
```py
import aiofiles

import tg_api


async def main(token: str, chat_id: int, photo_filename: str) -> None:
    async with tg_api.AsyncTgClient.setup(token):
        async with aiofiles.open(photo_filename, 'rb') as f:
            photo_content = await f.read()
        tg_request = tg_api.SendBytesPhotoRequest(chat_id=chat_id, photo=photo_content, filename=photo_filename)
        await tg_request.asend()
```


Пример отправки пользователю фото по URL:
```py
import tg_api


async def main(token: str, chat_id: int, photo_filename: str, photo_url: str) -> None:
    async with tg_api.AsyncTgClient.setup(token):
        tg_request = tg_api.SendUrlPhotoRequest(chat_id=chat_id, photo=photo_url, filename=photo_filename)
        await tg_request.asend()
```

Пример отправки пользователю документа из файловой системы:
```py
import aiofiles

import tg_api


async def main(token: str, chat_id: int, document_filename: str) -> None:
    async with tg_api.AsyncTgClient.setup(token):
        async with aiofiles.open(document_filename, 'rb') as f:
            document_content = await f.read()
        tg_request = tg_api.SendBytesDocumentRequest(chat_id=chat_id, document=document_content, filename=document_filename)
        await tg_request.asend()
```


Пример отправки пользователю документа по URL:
```py
import tg_api


async def main(token: str, chat_id: int, document_filename: str, document_url: str) -> None:
    async with tg_api.AsyncTgClient.setup(token):
        tg_request = tg_api.SendUrlDocumentRequest(chat_id=chat_id, document=document_url, filename=document_filename)
        await tg_request.asend()
```

<a name="usage-examples-low-level"></a>
### Низкоуровневое API

Низкоуровневое API позволяет использовать все самые свежие возможности [Telegram Bot API](https://core.telegram.org/bots/api), даже если их поддежку ещё не успели завезти
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

