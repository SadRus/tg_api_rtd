Добро пожаловать в документацию Tg API!
=====================================================

|PyPI - Downloads| |PyPI - License|

Библиотека Tg API упрощает работу с веб-API Telegram. Она предоставляет
тонкую обёртку над веб API Telegram и библиотекой
`HTTPX <https://www.python-httpx.org/>`__. Библиотека Tg API добавляет к
обычным возможностям HTTPX свои схемы данных и удобные часто используемые
функции, но не мешает, при необходимости, спускаться ниже на уровень
HTTP-запросов.

Ключевые возможности библиотеки Tg API:

-  Поддержка синхронных и асинхронных запросов к API
-  Shortcuts для часто используемых запросов
-  Лёгкий доступ к боту из любого места в коде
-  Наглядные схемы данных для всех типов запросов и ответов API
-  Аннотация типов для удобства работы с IDE
-  Простое низкоуровневое API для кастомизации запросов к API
-  Набор инструментов для удобной работы с исключениями

Пример отправки пользователю текстового сообщения:

.. code:: py

   from tg_api import SyncTgClient, SendMessageRequest


   with SyncTgClient.setup(token):
       tg_request = SendMessageRequest(chat_id=tg_chat_id, text='Hello user!')
       tg_request.send()


.. toctree::
   :maxdepth: 2
   :caption: The User Guide:

   quickstart
   advanced_usage

.. toctree::
   :maxdepth: 1
   :caption: API Reference:

   tg_methods
   tg_types


* :ref:`search`

.. |PyPI - Downloads| image:: https://img.shields.io/pypi/dm/tg_api
.. |PyPI - License| image:: https://img.shields.io/pypi/l/tg_api
