История релизов
===============

При очередном комите в файл записываем кратко смысл коммита, если были значимые изменения.

Изменения записываем в самый верх.

При публикации все изменения собираются в очередную версию.


Не в релизе
------------------------
- Зависимости библиотеки стали гибче, подходит любая версия httpx, начиная с 0.24.1 и pydantic v1 -- начиная с 1.10.8
- Из зависимостей библиотеки удалено лишнее: pytest, trio, anyio, exceptiongroup
- Добавлены описания полей в моделях tg_methods
- Добавлена модель ResponseParameters в tg_types
- Добавлено поле parameters в классе BaseTgResponse
- Добавлен валидатор для CallbackQuery для проверки наличия одного из полей (data/game_short_name)
- Добавлен автотест для проверки наличия одного из полей в CallbackQuery(data/game_short_name)


1.2.0 (2023-02-14)
------------------------

- Добавлены описания полей в моделях tg_types
- Модель CallbackQuery соотвествует документации
- Добавлены проверки на кнопки вызвавшие запрос
- Исправлен метод отправки запроса `EditBytesMessageMediaRequest` в случае пустых атрибутов `media.thumbnail` и/или `media.thumbnail_content`
- Исправлена схема SendBytesPhotoRequest: атрибут `photo` больше не разрешает `Iterable[bytes]`, принимает только `bytes`
- Добавлена поддержка mypy
- Исправлены поля модели `ChatMemberUpdated`

1.1.1 (2023-09-26)
------------------------

- Добавлены полезные ссылки на страницу либы на PyPI


1.1.0 (2023-09-26)
------------------------

- Добавлен конфиг `.readthedocs.yaml` и директория `sphinx_docs` с кофигурационными файлами для генерации API Reference
- Добавлены методы `EditBytesMessageMediaRequest`, `EditUrlMessageMediaRequest`, типы `InputMediaUrlPhoto`, `InputMediaBytesPhoto`, `InputMediaUrlDocument`, `InputMediaBytesDocument` для изменения медиа в сообщении
- Создан Makefile для основных команд проекта
- Добавлены методы `EditMessageCaptionResponse` и `EditMessageCaptionRequest` для изменения клавиатуры сообщения
- Добавлены методы `EditMessageReplyMarkupResponse` и `EditMessageReplyMarkupRequest` для изменения клавиатуры сообщения
- Добавлены методы `EditMessageTextResponse` и `EditMessageTextRequest` для изменения текста (и клавиатуры опционально) сообщения
- Увеличено количество поддерживаемых версий python(>=3.10), добавлены типы в tg_types для дочерних классов `ChatMember`
- Добавлены методы `DeleteMessageResponse` и `DeleteMessageRequest` для удаления сообщений
- Добавлены поля `my_chat_member` и `chat_member` в `tg_types.Update`, добавлен новый тип `ChatMemberUpdated`
- Добавлены тесты для `tg_methods.SendUrlPhotoRequest.send`, `asend` и `tg_methods.SendBytesPhotoRequest.send`, `asend`
- В README добавлены примеры для отправки фото и документа
- Добавлена проверка на пустой токен в синхронном и асинхронном клиентах
- Добавлены тесты для `tg_methods.SendUrlDocumentRequest.send`, `asend` и `tg_methods.SendBytesDocumentRequest.send`, `asend`
- В тесты добавлен общий модуль с фикстурами
- Исправлены типы в `tg_methods.SendBytesDocumentRequest`, в качестве параметра document теперь только bytes
- Добавлены тесты для `tg_types.Update`, `tg_methods.SendMessageRequest.send`, `asend`
- Добавлены тесты для `tg_types.InlineQuery`, `tg_methods.SendBytesPhotoRequest.send`, `asend`
- Библиотека докерезирована для разработки
- Добавлены тесты для tg_types.Message
- Добавлено ограничение на максимальное значение (4096 символов) текста в сообщении
- Добавлено ограничение на минимальную длину сообщений. Запрет отправки пустых сообщений
  или сообщений состоящих из пробельных символов
- Добавлено ограничение на максимальную длину для заголовка (caption) в 1024 символов

1.0.0 (2023-06-22)
------------------------

- Первый релиз
