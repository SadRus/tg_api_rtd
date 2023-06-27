import asks
import pytest
import json

from pytest_httpx import HTTPXMock
from tg_api.tg_types import Message, Chat, User
from tg_api import SendMessageResponse, AsyncTgClient, SendMessageRequest, SendBytesPhotoRequest


@pytest.fixture
async def get_response():
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


@pytest.mark.anyio()
async def test_httpx_mocking(
    httpx_mock: HTTPXMock,
    get_response,
):
    Chat.update_forward_refs()
    Message.update_forward_refs()
    httpx_mock.add_response(
        url='https://api.telegram.org/bottoken/sendMessage',
        method='POST',
        headers={
            'content-type': 'application/json',
            'accept': 'application/json',
        },
        json=get_response,
    )

    async with AsyncTgClient.setup('token'):
        tg_request = SendMessageRequest(chat_id=1234567890, text='Hello World!')
        json_payload = await tg_request.apost_as_json('sendMessage')
        response = await tg_request.asend()
        assert get_response == json.loads(json_payload)
        assert get_response == response.dict()
        assert isinstance(response, SendMessageResponse)


@pytest.mark.anyio()
async def test_photo_request(
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
    response = await asks.get(photo_url)

    async with AsyncTgClient.setup('token'):
        tg_request = SendBytesPhotoRequest(
            chat_id=1234567890,
            photo=str(response.content),
        )
        json_payload = await tg_request.apost_as_json('sendPhoto')
        response = await tg_request.asend()
        assert get_response == json.loads(json_payload)
        assert get_response == response.dict()
