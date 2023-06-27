import requests
import json

import pytest_httpx
from tg_api import tg_methods, tg_types


def test_photo_request(
    httpx_mock: pytest_httpx.HTTPXMock,
    get_message_response: tg_methods.SendMessageResponse,
):
    tg_types.Chat.update_forward_refs()
    tg_types.Message.update_forward_refs()
    httpx_mock.add_response(
        url='https://api.telegram.org/bottoken/sendPhoto',
        method='POST',
        headers={
            'content-type': 'application/json',
            'accept': 'application/json',
        },
        json=get_message_response,
    )

    photo_url = 'https://memepedia.ru/wp-content/uploads/2018/06/kto-prochital-tot-sdohnet.jpg'
    response = requests.get(photo_url)
    response.raise_for_status()

    with tg_methods.SyncTgClient.setup('token'):
        tg_request = tg_methods.SendBytesPhotoRequest(
            chat_id=1234567890,
            photo=str(response.content),
        )
        json_payload = tg_request.post_as_json('sendPhoto')
        response = tg_request.send()
        assert get_message_response == json.loads(json_payload)
        assert get_message_response == response.dict()


def test_message_request(
    httpx_mock: pytest_httpx.HTTPXMock,
    get_message_response: tg_methods.SendMessageResponse,
):
    httpx_mock.add_response(
        url='https://api.telegram.org/bottoken/sendMessage',
        method='POST',
        headers={
            'content-type': 'application/json',
            'accept': 'application/json',
        },
        json=get_message_response,
    )

    with tg_methods.SyncTgClient.setup('token'):
        tg_request = tg_methods.SendMessageRequest(chat_id=1234567890, text='Hello World!')
        json_payload = tg_request.post_as_json('sendMessage')
        response = tg_request.send()
        assert isinstance(response, tg_methods.SendMessageResponse)
        assert get_message_response == json.loads(json_payload)
        assert get_message_response == response.dict()
