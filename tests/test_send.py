import requests
import json

from pytest_httpx import HTTPXMock
from tg_api.tg_types import Message, Chat
from tg_api import SendMessageResponse, SyncTgClient, SendMessageRequest, SendBytesPhotoRequest


def test_photo_request(
    httpx_mock: HTTPXMock,
    get_message_response: SendMessageResponse,
):
    Chat.update_forward_refs()
    Message.update_forward_refs()
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

    with SyncTgClient.setup('token'):
        tg_request = SendBytesPhotoRequest(
            chat_id=1234567890,
            photo=str(response.content),
        )
        json_payload = tg_request.post_as_json('sendPhoto')
        response = tg_request.send()
        assert get_message_response == json.loads(json_payload)
        assert get_message_response == response.dict()


def test_message_request(
    httpx_mock: HTTPXMock,
    get_message_response: SendMessageResponse,
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

    with SyncTgClient.setup('token'):
        tg_request = SendMessageRequest(chat_id=1234567890, text='Hello World!')
        json_payload = tg_request.post_as_json('sendMessage')
        response = tg_request.send()
        assert isinstance(response, SendMessageResponse)
        assert get_message_response == json.loads(json_payload)
        assert get_message_response == response.dict()
