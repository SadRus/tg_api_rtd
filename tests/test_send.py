import json
import requests
import pytest_httpx
from tg_api import tg_methods, tg_types


def test_photo_request_mocking(
    httpx_mock: pytest_httpx.HTTPXMock,
    get_photo_response: tg_methods.SendPhotoResponse,
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
        json=get_photo_response,
    )

    photo_url = 'https://memepedia.ru/wp-content/uploads/2018/06/kto-prochital-tot-sdohnet.jpg'
    response = requests.get(photo_url)
    response.raise_for_status()

    with tg_methods.SyncTgClient.setup('token'):
        tg_request = tg_methods.SendBytesPhotoRequest(
            chat_id=1234567890,
            photo=str(response.content),
            caption_entities=[tg_types.MessageEntity(type='123', offset=1, length=1)],
            reply_markup=tg_types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [tg_types.InlineKeyboardButton(text='123')],
                ],
            ),
        )
        json_payload = tg_request.post_as_json('sendPhoto')
        response = tg_request.send()
        assert get_photo_response == json.loads(json_payload)
        assert get_photo_response == response.dict()

    with tg_methods.SyncTgClient.setup('token'):
        tg_request = tg_methods.SendUrlPhotoRequest(
            chat_id=1234567890,
            photo=photo_url,
            caption_entities=[tg_types.MessageEntity(type='123', offset=1, length=1)],
            reply_markup=tg_types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [tg_types.InlineKeyboardButton(text='123')],
                ],
            ),
        )
        json_payload = tg_request.post_as_json('sendPhoto')
        response = tg_request.send()
        assert get_photo_response == json.loads(json_payload)
        assert get_photo_response == response.dict()


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


def test_document_request_mocking(
    httpx_mock: pytest_httpx.HTTPXMock,
    get_document_response: tg_methods.SendDocumentResponse,
):
    tg_types.Chat.update_forward_refs()
    tg_types.Message.update_forward_refs()
    httpx_mock.add_response(
        url='https://api.telegram.org/bottoken/sendDocument',
        method='POST',
        headers={
            'content-type': 'application/json',
            'accept': 'application/json',
        },
        json=get_document_response,
    )

    objects_which_pydantic_transforms_to_bytes_or_iterable_bytes = [
        bytes('document content', encoding='utf8'),
        b'document content',
        '123',
        123,
    ]

    for obj in objects_which_pydantic_transforms_to_bytes_or_iterable_bytes:
        with tg_methods.SyncTgClient.setup('token'):
            tg_request = tg_methods.SendBytesDocumentRequest(
                chat_id=1234567890,
                document=obj,
                filename='filename.csv',
                caption_entities=[tg_types.MessageEntity(type='123', offset=1, length=1)],
                reply_markup=tg_types.InlineKeyboardMarkup(
                    inline_keyboard=[
                        [tg_types.InlineKeyboardButton(text='123')],
                    ],
                ),
            )
            json_payload = tg_request.post_as_json('sendDocument')
            response = tg_request.send()
            assert get_document_response == json.loads(json_payload)
            assert get_document_response == response.dict()

    objects_which_pydantic_transforms_to_str = [
        'document content',
        b'document content',
        123,
    ]

    for obj in objects_which_pydantic_transforms_to_str:
        with tg_methods.SyncTgClient.setup('token'):
            tg_request = tg_methods.SendUrlDocumentRequest(
                chat_id=1234567890,
                document=obj,
                filename='filename.csv',
                caption_entities=[tg_types.MessageEntity(type='123', offset=1, length=1)],
                reply_markup=tg_types.InlineKeyboardMarkup(
                    inline_keyboard=[
                        [tg_types.InlineKeyboardButton(text='123')],
                    ],
                ),
            )
            json_payload = tg_request.post_as_json('sendDocument')
            response = tg_request.send()
            assert get_document_response == json.loads(json_payload)
            assert get_document_response == response.dict()
