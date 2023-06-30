История релизов
===============

Образец файла взят из библиотеки request.

При очередном комите в файл записываем кратко смысл коммита, если были значимые изменения.

Изменения записываем в самый верх.

При публикации все изменения собираются в очередную версию.


Не в релизе
------------------------

- Добавлены поля my_chat_member и chat_member в tg_types.Update, добавлен новый тип ChatMemberUpdated
- Добавлены тесты для tg_methods.SendUrlPhotoRequest.send, asend и tg_methods.SendBytesPhotoRequest.send, asend
- В README добавлены примеры для отправки фото и документа
- Добавлена проверка на пустой токен в синхронном и асинхронном клиентах
- Добавлены тесты для tg_methods.SendUrlDocumentRequest.send, asend и tg_methods.SendBytesDocumentRequest.send, asend
- В тесты добавлен общий модуль с фикстурами
- Исправлены типы в tg_methods.SendBytesDocumentRequest, в качестве параметра document теперь только bytes
- Добавлены тесты для tg_types.Update, tg_methods.SendMessageRequest.send, asend
- Добавлены тесты для tg_types.InlineQuery, tg_methods.SendBytesPhotoRequest.send, asend
- Библиотека докерезирована для разработки
- Добавлены тесты для tg_types.Message

1.0.0 (2023-06-22)
------------------------

- Первый релиз