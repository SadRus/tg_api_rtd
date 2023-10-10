import typing

import pytest
import requests
from pydantic import ValidationError

from tg_api import tg_methods, tg_types


def test_photo_request_mocking_with_large_caption(
    get_photo_response: dict[str, typing.Any],
):
    '''
    Программист - Узнавать о длинных заголовках сообщений до отправки запроса к серверу Telegram
    при отправке SendBytesPhotoRequest: !func
        Проверить срабатывание ValidationError до отправки сообщений: !story
            сделано: yes
            старт: Отправка заголовка свыше 1024 символов
            успех: Сработало исключение до отправки сообщения к серверу
    '''

    tg_types.Chat.update_forward_refs()
    tg_types.Message.update_forward_refs()

    photo_url = 'https://memepedia.ru/wp-content/uploads/2018/06/kto-prochital-tot-sdohnet.jpg'
    response = requests.get(photo_url)
    response.raise_for_status()

    with tg_methods.SyncTgClient.setup('token'):
        with pytest.raises(ValidationError):
            tg_methods.SendBytesPhotoRequest(
                chat_id=1234567890,
                caption='a' * 1025,
                photo=str(response.content),
                caption_entities=[tg_types.MessageEntity(type='123', offset=1, length=1)],
                reply_markup=tg_types.InlineKeyboardMarkup(
                    inline_keyboard=[
                        [tg_types.InlineKeyboardButton(text='123')],
                    ],
                ),
            )

    with tg_methods.SyncTgClient.setup('token'):
        with pytest.raises(ValidationError):
            tg_methods.SendUrlPhotoRequest(
                chat_id=1234567890,
                photo=photo_url,
                caption='a' * 1025,
                caption_entities=[tg_types.MessageEntity(type='123', offset=1, length=1)],
                reply_markup=tg_types.InlineKeyboardMarkup(
                    inline_keyboard=[
                        [tg_types.InlineKeyboardButton(text='123')],
                    ],
                ),
            )


def test_message_request_with_large_text(
    get_message_response: dict[str, typing.Any],
):
    '''
    Программист - Узнавать о длинных сообщениях до отправки запроса к серверу Telegram
    при отправке SendMessageRequest: !func
        Проверить срабатывание ValidationError до отправки сообщений: !story
            сделано: yes
            старт: Отправка сообщения свыше 4096 символов
            успех: Сработало исключение до отправки сообщения к серверу
    '''

    with tg_methods.SyncTgClient.setup('token'):
        with pytest.raises(ValidationError):
            tg_methods.SendMessageRequest(
                chat_id=1234567890,
                text='a' * 4097
            )


def test_message_request_with_empty_text(
    get_message_response: dict[str, typing.Any],
):
    '''
    Программист - Узнавать о пустых сообщениях до отправки запроса к серверу Telegram
    при отправке SendMessageRequest: !func
        Проверить срабатывание ValidationError до отправки сообщений: !story
            сделано: yes
            старт: Отправка пустого сообщения и сообщения из пробельных символов
            успех: Сработало исключение до отправки сообщения к серверу
    '''

    with tg_methods.SyncTgClient.setup('token'):
        with pytest.raises(ValidationError):
            tg_methods.SendMessageRequest(
                chat_id=1234567890,
                text=''
            )

    with tg_methods.SyncTgClient.setup('token'):
        with pytest.raises(ValidationError):
            tg_methods.SendMessageRequest(
                chat_id=1234567890,
                text='   '
            )


def test_document_request_mocking_with_large_caption(
    get_document_response: dict[str, typing.Any],
):
    '''
    Программист - Узнавать о длинных заголовках сообщений до отправки запроса к серверу Telegram
    при отправке SendBytesDocumentRequest: !func
        Проверить срабатывание ValidationError до отправки сообщений: !story
            сделано: yes
            старт: Отправка заголовка свыше 1024 символов
            успех: Сработало исключение до отправки сообщения к серверу
    '''
    tg_types.Chat.update_forward_refs()
    tg_types.Message.update_forward_refs()

    objects_which_pydantic_transforms_to_bytes_or_iterable_bytes = [
        bytes('document content', encoding='utf8'),
        b'document content',
        '123',
        123,
    ]

    for obj in objects_which_pydantic_transforms_to_bytes_or_iterable_bytes:
        with tg_methods.SyncTgClient.setup('token'):
            with pytest.raises(ValidationError):
                tg_methods.SendBytesDocumentRequest(
                    chat_id=1234567890,
                    caption="a" * 1025,
                    document=obj,
                    filename='filename.csv',
                    caption_entities=[tg_types.MessageEntity(type='123', offset=1, length=1)],
                    reply_markup=tg_types.InlineKeyboardMarkup(
                        inline_keyboard=[
                            [tg_types.InlineKeyboardButton(text='123')],
                        ],
                    ),
                )

    objects_which_pydantic_transforms_to_str = [
        'document content',
        b'document content',
        123,
    ]

    for obj in objects_which_pydantic_transforms_to_str:
        with tg_methods.SyncTgClient.setup('token'):
            with pytest.raises(ValidationError):
                tg_methods.SendUrlDocumentRequest(
                    chat_id=1234567890,
                    caption="a" * 1025,
                    document=obj,
                    filename='filename.csv',
                    caption_entities=[tg_types.MessageEntity(type='123', offset=1, length=1)],
                    reply_markup=tg_types.InlineKeyboardMarkup(
                        inline_keyboard=[
                            [tg_types.InlineKeyboardButton(text='123')],
                        ],
                    ),
                )


def test_edit_message_text_request_mocking_with_large_text(
    edit_message_text_response: dict[str, typing.Any],
    keyboard: tg_types.InlineKeyboardMarkup,
):
    '''
    Программист - Узнавать о длинных сообщениях до отправки запроса к серверу Telegram
    при отправке EditMessageTextRequest: !func
        Проверить срабатывание ValidationError до отправки сообщений: !story
            сделано: yes
            старт: Отправка сообщения свыше 4096 символов
            успех: Сработало исключение до отправки сообщения к серверу
    '''

    with tg_methods.SyncTgClient.setup('token'):
        with pytest.raises(ValidationError):
            tg_methods.EditMessageTextRequest(
                chat_id=1234567890,
                message_id=12345,
                text='a' * 4097,
            )

def test_edit_message_text_request_mocking_with_empty_text(
    edit_message_text_response: dict[str, typing.Any],
    keyboard: tg_types.InlineKeyboardMarkup,
):
    '''
    Программист - Узнавать о пустых сообщениях до отправки запроса к серверу Telegram
    при отправке EditMessageTextRequest: !func
        Проверить срабатывание ValidationError до отправки сообщений: !story
            сделано: yes
            старт: Отправка пустого сообщения и сообщения из пробельных символов
            успех: Сработало исключение до отправки сообщения к серверу
    '''

    with tg_methods.SyncTgClient.setup('token'):
        with pytest.raises(ValidationError):
            tg_methods.EditMessageTextRequest(
                chat_id=1234567890,
                message_id=12345,
                text='',
            )

    with tg_methods.SyncTgClient.setup('token'):
        with pytest.raises(ValidationError):
            tg_methods.EditMessageTextRequest(
                chat_id=1234567890,
                message_id=12345,
                text='  ',
            )
def test_edit_message_caption_request_mocking_with_large_caption(
    edit_message_caption_response: dict[str, typing.Any],
):
    '''
    Программист - Узнавать о длинных заголовках сообщений до отправки запроса к серверу Telegram
    при отправке EditMessageCaptionRequest: !func
        Проверить срабатывание ValidationError до отправки сообщений: !story
            сделано: yes
            старт: Отправка заголовка свыше 1024 символов
            успех: Сработало исключение до отправки сообщения к серверу
    '''

    with tg_methods.SyncTgClient.setup('token'):
        with pytest.raises(ValidationError):
            tg_methods.EditMessageCaptionRequest(
                chat_id=1234567890,
                message_id=12345,
                caption='a' * 1025,
            )


def test_edit_message_media_url_photo_request_mocking_with_large_caption(
    edit_message_media_photo_response: dict[str, typing.Any],
):
    '''
    Программист - Узнавать о длинных заголовках сообщений до отправки запроса к серверу Telegram
    при отправке EditUrlMessageMediaRequest: !func
        Проверить срабатывание ValidationError до отправки сообщений: !story
            сделано: yes
            старт: Отправка заголовка свыше 1024 символов
            успех: Сработало исключение до отправки сообщения к серверу
    '''

    with tg_methods.SyncTgClient.setup('token'):
        with pytest.raises(ValidationError):
            media = tg_types.InputMediaUrlPhoto(
                media='https://link_to_photo.jpg',
                caption='a' * 1025,
            )
            tg_methods.EditUrlMessageMediaRequest(
                chat_id=1234567890,
                message_id=12345,
                media=media,
            )


def test_edit_message_media_url_document_request_mocking(
    edit_message_media_document_response: dict[str, typing.Any],
):
    '''
    Программист - Узнавать о длинных заголовках сообщений до отправки запроса к серверу Telegram
    при отправке EditUrlMessageMediaRequest: !func
        Проверить срабатывание ValidationError до отправки сообщений: !story
            сделано: yes
            старт: Отправка заголовка свыше 1024 символов
            успех: Сработало исключение до отправки сообщения к серверу
    '''

    with tg_methods.SyncTgClient.setup('token'):
        with pytest.raises(ValidationError):
            media = tg_types.InputMediaUrlDocument(
                media='https://link_to_document.pdf',
                caption='a' * 1025,
            )
            tg_methods.EditUrlMessageMediaRequest(
                chat_id=1234567890,
                message_id=12345,
                media=media,
            )


def test_edit_message_media_bytes_photo_request_mocking(
    edit_message_media_photo_response: dict[str, typing.Any],
):
    '''
    Программист - Узнавать о длинных заголовках сообщений до отправки запроса к серверу Telegram
    при отправке EditBytesMessageMediaRequest: !func
        Проверить срабатывание ValidationError до отправки сообщений: !story
            сделано: yes
            старт: Отправка заголовка свыше 1024 символов
            успех: Сработало исключение до отправки сообщения к серверу
    '''

    with tg_methods.SyncTgClient.setup('token'):
        with pytest.raises(ValidationError):
            media = tg_types.InputMediaBytesPhoto(
                media='attach://attachement.jpg',
                media_content=b'photo content',
                caption='a' * 1025,
            )
            tg_methods.EditBytesMessageMediaRequest(
                chat_id=1234567890,
                message_id=12345,
                media=media,
            )


def test_edit_message_media_bytes_document_request_mocking(
    edit_message_media_document_response: dict[str, typing.Any],
):
    '''
    Программист - Узнавать о длинных заголовках сообщений до отправки запроса к серверу Telegram
    при отправке EditBytesMessageMediaRequest: !func
        Проверить срабатывание ValidationError до отправки сообщений: !story
            сделано: yes
            старт: Отправка заголовка свыше 1024 символов
            успех: Сработало исключение до отправки сообщения к серверу
    '''

    with tg_methods.SyncTgClient.setup('token'):
        with pytest.raises(ValidationError):
            media = tg_types.InputMediaBytesDocument(
                media='attach://attachement.pdf',
                media_content=b'document content',
                caption='a' * 1025,
            )
            tg_methods.EditBytesMessageMediaRequest(
                chat_id=1234567890,
                message_id=12345,
                media=media,
            )
