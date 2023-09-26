import json
import typing

import requests
import pytest
import pytest_httpx

from tg_bot_api import tg_methods, tg_types


@pytest.mark.anyio
async def test_httpx_mocking(
    httpx_mock: pytest_httpx.HTTPXMock,
    get_message_response: dict[str, typing.Any],
):
    tg_types.Chat.update_forward_refs()
    tg_types.Message.update_forward_refs()
    httpx_mock.add_response(
        url='https://api.telegram.org/bottoken/sendMessage',
        method='POST',
        headers={
            'content-type': 'application/json',
            'accept': 'application/json',
        },
        json=get_message_response,
    )

    async with tg_methods.AsyncTgClient.setup('token'):
        tg_request = tg_methods.SendMessageRequest(chat_id=1234567890, text='Hello World!')
        json_payload = await tg_request.apost_as_json('sendMessage')
        response = await tg_request.asend()
        assert get_message_response == json.loads(json_payload)
        assert get_message_response == response.dict()
        assert isinstance(response, tg_methods.SendMessageResponse)


@pytest.mark.anyio
async def test_photo_request_mocking(
    httpx_mock: pytest_httpx.HTTPXMock,
    get_photo_response: dict[str, typing.Any],
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

    async with tg_methods.AsyncTgClient.setup('token'):
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
        json_payload = await tg_request.apost_as_json('sendPhoto')
        response = await tg_request.asend()
        assert get_photo_response == json.loads(json_payload)
        assert get_photo_response == response.dict()

    async with tg_methods.AsyncTgClient.setup('token'):
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
        json_payload = await tg_request.apost_as_json('sendPhoto')
        response = await tg_request.asend()
        assert get_photo_response == json.loads(json_payload)
        assert get_photo_response == response.dict()


@pytest.mark.anyio
async def test_document_request_mocking(
    httpx_mock: pytest_httpx.HTTPXMock,
    get_document_response: dict[str, typing.Any],
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
        async with tg_methods.AsyncTgClient.setup('token'):
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
            json_payload = await tg_request.apost_as_json('sendDocument')
            response = await tg_request.asend()
            assert get_document_response == json.loads(json_payload)
            assert get_document_response == response.dict()

    objects_which_pydantic_transforms_to_str = [
        'document content',
        b'document content',
        123,
    ]

    for obj in objects_which_pydantic_transforms_to_str:
        async with tg_methods.AsyncTgClient.setup('token'):
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
            json_payload = await tg_request.apost_as_json('sendDocument')
            response = await tg_request.asend()
            assert get_document_response == json.loads(json_payload)
            assert get_document_response == response.dict()


@pytest.mark.anyio
async def test_delete_message_request_mocking(
    httpx_mock: pytest_httpx.HTTPXMock,
    delete_message_response: dict[str, typing.Any],
):
    tg_types.Chat.update_forward_refs()
    tg_types.Message.update_forward_refs()
    httpx_mock.add_response(
        url='https://api.telegram.org/bottoken/deleteMessage',
        method='POST',
        headers={
            'content-type': 'application/json',
            'accept': 'application/json',
        },
        json=delete_message_response,
    )

    async with tg_methods.AsyncTgClient.setup('token'):
        tg_request = tg_methods.DeleteMessageRequest(chat_id=1234567890, message_id=12345)
        json_payload = await tg_request.apost_as_json('deleteMessage')
        response = await tg_request.asend()
        assert isinstance(response, tg_methods.DeleteMessageResponse)
        assert delete_message_response == json.loads(json_payload)
        assert delete_message_response == response.dict()


@pytest.mark.anyio
async def test_edit_message_text_request_mocking(
    httpx_mock: pytest_httpx.HTTPXMock,
    edit_message_text_response: dict[str, typing.Any],
    keyboard: tg_types.InlineKeyboardMarkup,
):
    tg_types.Chat.update_forward_refs()
    tg_types.Message.update_forward_refs()
    httpx_mock.add_response(
        url='https://api.telegram.org/bottoken/editmessagetext',
        method='POST',
        headers={
            'content-type': 'application/json',
            'accept': 'application/json',
        },
        json=edit_message_text_response,
    )

    async with tg_methods.AsyncTgClient.setup('token'):
        tg_request = tg_methods.EditMessageTextRequest(
            chat_id=1234567890,
            message_id=12345,
            text='Edited text',
            reply_markup=keyboard,
        )
        json_payload = await tg_request.apost_as_json('editmessagetext')
        response = await tg_request.asend()
        assert isinstance(response, tg_methods.EditMessageTextResponse)
        assert edit_message_text_response == json.loads(json_payload)
        assert edit_message_text_response == response.dict()


@pytest.mark.anyio
async def test_edit_message_reply_markup_request_mocking(
    httpx_mock: pytest_httpx.HTTPXMock,
    edit_message_reply_markup_response: dict[str, typing.Any],
    keyboard: tg_types.InlineKeyboardMarkup,
):
    tg_types.Chat.update_forward_refs()
    tg_types.Message.update_forward_refs()
    httpx_mock.add_response(
        url='https://api.telegram.org/bottoken/editmessagereplymarkup',
        method='POST',
        headers={
            'content-type': 'application/json',
            'accept': 'application/json',
        },
        json=edit_message_reply_markup_response,
    )

    async with tg_methods.AsyncTgClient.setup('token'):
        tg_request = tg_methods.EditMessageReplyMarkupRequest(
            chat_id=1234567890,
            message_id=12345,
            reply_markup=keyboard,
        )
        json_payload = await tg_request.apost_as_json('editmessagereplymarkup')
        response = await tg_request.asend()
        assert isinstance(response, tg_methods.EditMessageReplyMarkupResponse)
        assert edit_message_reply_markup_response == json.loads(json_payload)
        assert edit_message_reply_markup_response == response.dict()


@pytest.mark.anyio
async def test_edit_message_caption_request_mocking(
    httpx_mock: pytest_httpx.HTTPXMock,
    edit_message_caption_response: dict[str, typing.Any],
):
    tg_types.Chat.update_forward_refs()
    tg_types.Message.update_forward_refs()
    httpx_mock.add_response(
        url='https://api.telegram.org/bottoken/editmessagecaption',
        method='POST',
        headers={
            'content-type': 'application/json',
            'accept': 'application/json',
        },
        json=edit_message_caption_response,
    )

    async with tg_methods.AsyncTgClient.setup('token'):
        tg_request = tg_methods.EditMessageCaptionRequest(
            chat_id=1234567890,
            message_id=12345,
            caption='edited caption',
        )
        json_payload = await tg_request.apost_as_json('editmessagecaption')
        response = await tg_request.asend()
        assert isinstance(response, tg_methods.EditMessageCaptionResponse)
        assert edit_message_caption_response == json.loads(json_payload)
        assert edit_message_caption_response == response.dict()


@pytest.mark.anyio
async def test_edit_message_media_url_photo_request_mocking(
    httpx_mock: pytest_httpx.HTTPXMock,
    edit_message_media_photo_response: dict[str, typing.Any],
):
    tg_types.Chat.update_forward_refs()
    tg_types.Message.update_forward_refs()
    httpx_mock.add_response(
        url='https://api.telegram.org/bottoken/editmessagemedia',
        method='POST',
        headers={
            'content-type': 'application/json',
            'accept': 'application/json',
        },
        json=edit_message_media_photo_response,
    )

    async with tg_methods.AsyncTgClient.setup('token'):
        media = tg_types.InputMediaUrlPhoto(
            media='https://link_to_photo.jpg',
            caption='edited caption',
        )
        tg_request = tg_methods.EditUrlMessageMediaRequest(
            chat_id=1234567890,
            message_id=12345,
            media=media,
        )
        json_payload = await tg_request.apost_as_json('editmessagemedia')
        response = await tg_request.asend()
        assert isinstance(response, tg_methods.EditMessageMediaResponse)
        assert edit_message_media_photo_response == json.loads(json_payload)
        assert edit_message_media_photo_response == response.dict()


@pytest.mark.anyio
async def test_edit_message_media_url_document_request_mocking(
    httpx_mock: pytest_httpx.HTTPXMock,
    edit_message_media_document_response: dict[str, typing.Any],
):
    tg_types.Chat.update_forward_refs()
    tg_types.Message.update_forward_refs()
    httpx_mock.add_response(
        url='https://api.telegram.org/bottoken/editmessagemedia',
        method='POST',
        headers={
            'content-type': 'application/json',
            'accept': 'application/json',
        },
        json=edit_message_media_document_response,
    )

    async with tg_methods.AsyncTgClient.setup('token'):
        media = tg_types.InputMediaUrlDocument(
            media='https://link_to_document.pdf',
            caption='edited caption',
        )
        tg_request = tg_methods.EditUrlMessageMediaRequest(
            chat_id=1234567890,
            message_id=12345,
            media=media,
        )
        json_payload = await tg_request.apost_as_json('editmessagemedia')
        response = await tg_request.asend()
        assert isinstance(response, tg_methods.EditMessageMediaResponse)
        assert edit_message_media_document_response == json.loads(json_payload)
        assert edit_message_media_document_response == response.dict()


@pytest.mark.anyio
async def test_edit_message_media_bytes_photo_request_mocking(
    httpx_mock: pytest_httpx.HTTPXMock,
    edit_message_media_photo_response: dict[str, typing.Any],
):
    tg_types.Chat.update_forward_refs()
    tg_types.Message.update_forward_refs()
    httpx_mock.add_response(
        url='https://api.telegram.org/bottoken/editmessagemedia',
        method='POST',
        headers={
            'content-type': 'application/json',
            'accept': 'application/json',
        },
        json=edit_message_media_photo_response,
    )

    async with tg_methods.AsyncTgClient.setup('token'):
        media = tg_types.InputMediaBytesPhoto(
            media='attach://attachement.jpg',
            media_content=b'photo content',
            caption='edited caption',
        )
        tg_request = tg_methods.EditBytesMessageMediaRequest(
            chat_id=1234567890,
            message_id=12345,
            media=media,
        )
        json_payload = await tg_request.apost_as_json('editmessagemedia')
        response = await tg_request.asend()
        assert isinstance(response, tg_methods.EditMessageMediaResponse)
        assert edit_message_media_photo_response == json.loads(json_payload)
        assert edit_message_media_photo_response == response.dict()


@pytest.mark.anyio
async def test_edit_message_media_bytes_document_request_mocking(
    httpx_mock: pytest_httpx.HTTPXMock,
    edit_message_media_document_response: dict[str, typing.Any],
):
    tg_types.Chat.update_forward_refs()
    tg_types.Message.update_forward_refs()
    httpx_mock.add_response(
        url='https://api.telegram.org/bottoken/editmessagemedia',
        method='POST',
        headers={
            'content-type': 'application/json',
            'accept': 'application/json',
        },
        json=edit_message_media_document_response,
    )

    async with tg_methods.AsyncTgClient.setup('token'):
        media = tg_types.InputMediaBytesDocument(
            media='attach://attachement.pdf',
            media_content=b'document content',
            caption='edited caption',
        )
        tg_request = tg_methods.EditBytesMessageMediaRequest(
            chat_id=1234567890,
            message_id=12345,
            media=media,
        )
        json_payload = await tg_request.apost_as_json('editmessagemedia')
        response = await tg_request.asend()
        assert isinstance(response, tg_methods.EditMessageMediaResponse)
        assert edit_message_media_document_response == json.loads(json_payload)
        assert edit_message_media_document_response == response.dict()
