Advanced Usage
==============

Низкоуровневое API
------------------

Низкоуровневое API позволяет использовать все самые свежие возможности
`Telegram Bot API <https://core.telegram.org/bots/api>`__, даже если их
поддежку ещё не успели завезти в библиотеку Tg API. Можно добавлять свои
типы запросов и ответов API, менять способ отправки HTTP-запросов и
реакции на ответ.

Пример использования низкоуровневого асинхронного API:

.. code:: py

   from httpx import Response as HttpResponse
   from tg_api import (
       AsyncTgClient,
       SendMessageRequest,
       SendMessageResponse,
       raise_for_tg_response_status,
   )


   async def main(token: str, chat_id: int) -> None:
       async with AsyncTgClient.setup(token) as tg_client:
           tg_request = SendMessageRequest(
               chat_id=chat_id,
               text='Message proofs low level API usage.',
           )
           json_bytes = tg_request.json(exclude_none=True).encode('utf-8')

           http_response: HttpResponse = await tg_client.session.post(
               f'{tg_client.api_root}sendMessage',
               headers={'content-type': 'application/json'},
               content=json_bytes,
           )
           # поднимет исключение TgRuntimeError если сервер Telegram ответит
           # на запрос HTTP статусом != 2xx
           raise_for_tg_response_status(http_response)

           tg_response = SendMessageResponse.parse_raw(http_response.content)
           print('Id нового сообщения:', tg_response.result.message_id)
