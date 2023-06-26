import requests
import pytest
import json

from pytest_httpx import HTTPXMock
from tg_api.tg_types import Message, Chat, User
from tg_api import SendMessageResponse, SyncTgClient, SendMessageRequest, SendBytesPhotoRequest, SendPhotoResponse


@pytest.fixture
def get_response():
    return SendMessageResponse.parse_obj(
        {
            'ok': True,
            'result': Message.parse_obj({
                'chat': Chat.parse_obj({
                    'first_name': 'TestFirstName',
                    'id': 1234567890,
                    'last_name': 'TestLastName',
                    'type': 'private',
                    'username': 'TestUserName',
                }),
                'date': 1686840262,
                'from_': User.parse_obj({
                    'first_name': 'TestFirstName',
                    'id': 1234567890,
                    'is_bot': False,
                    'language_code': 'ru',
                    'last_name': 'TestLastName',
                    'username': 'TestUserName',
                }),
                'message_id': 12345,
                'text': 'Hello World!',
            }),
        },
    ).dict()


def test_photo_request(
    httpx_mock: HTTPXMock,
    get_response,
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
        json=get_response,
    )

    photo_url = 'https://memepedia.ru/wp-content/uploads/2018/06/kto-prochital-tot-sdohnet.jpg'
    response = requests.get(photo_url)
    response.raise_for_status()

    with SyncTgClient.setup('token'):
        tg_request = SendBytesPhotoRequest(
            chat_id=1234567890,
            photo=str(response.content)
        )
        json_payload = tg_request.post_as_json('sendPhoto')
        response = tg_request.send()
        assert get_response == json.loads(json_payload)
        assert get_response == response.dict()


@pytest.fixture
def get_response():
    return SendMessageResponse.parse_obj(
        {
            'ok': True,
            'result': Message.parse_obj({
                'chat': Chat.parse_obj({
                    'first_name': 'TestFirstName',
                    'id': 1234567890,
                    'last_name': 'TestLastName',
                    'type': 'private',
                    'username': 'TestUserName',
                }),
                'date': 1686840262,
                'from_': User.parse_obj({
                    'first_name': 'TestFirstName',
                    'id': 1234567890,
                    'is_bot': False,
                    'language_code': 'ru',
                    'last_name': 'TestLastName',
                    'username': 'TestUserName',
                }),
                'message_id': 12345,
                'text': 'Hello World!',
            }),
        },
    ).dict()


def test_message_request(
    httpx_mock: HTTPXMock,
    get_response,
):
    httpx_mock.add_response(
        url='https://api.telegram.org/bottoken/sendMessage',
        method='POST',
        headers={
            'content-type': 'application/json',
            'accept': 'application/json',
        },
        json=get_response,
    )

    with SyncTgClient.setup('token'):
        tg_request = SendMessageRequest(chat_id=1234567890, text='Hello World!')
        json_payload = tg_request.post_as_json('sendMessage')
        response = tg_request.send()
        assert isinstance(response, SendMessageResponse)
        assert get_response == json.loads(json_payload)
        assert get_response == response.dict()
