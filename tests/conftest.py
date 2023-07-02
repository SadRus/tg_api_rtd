import typing

import pytest

from tg_api import tg_types, tg_methods


@pytest.fixture
def get_message_response() -> dict[str, typing.Any]:
    return tg_methods.SendMessageResponse.parse_obj(
        {
            'ok': True,
            'result': tg_types.Message.parse_obj({
                'chat': tg_types.Chat.parse_obj({
                    'first_name': 'TestFirstName',
                    'id': 1234567890,
                    'last_name': 'TestLastName',
                    'type': 'private',
                    'username': 'TestUserName',
                }),
                'date': 1686840262,
                'from_': tg_types.User.parse_obj({
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


@pytest.fixture
def get_document_response() -> dict[str, typing.Any]:
    return tg_methods.SendDocumentResponse.parse_obj(
        {
            'ok': True,
            'result': tg_types.Message.parse_obj({
                'chat': tg_types.Chat.parse_obj({
                    'first_name': 'TestFirstName',
                    'id': 1234567890,
                    'last_name': 'TestLastName',
                    'type': 'private',
                    'username': 'TestUserName',
                }),
                'date': 1686840262,
                'from_': tg_types.User.parse_obj({
                    'first_name': 'TestFirstName',
                    'id': 1234567890,
                    'is_bot': False,
                    'language_code': 'ru',
                    'last_name': 'TestLastName',
                    'username': 'TestUserName',
                }),
                'message_id': 12345,
                "document": {
                    "file_name": "document.csv",
                    "mime_type": "text/csv",
                    "file_id": "BQACAgIAAxkBAAMQZJRQU7dV3gHKrckVBQk4NAoy5TsAAvw2AAJq0KlIIuX8ICpuOOwvBA",
                    "file_unique_id": "AgAD_DYAAmrQqUg",
                    "file_size": 48,
                },
                "caption": "test caption",
            }),
        },
    ).dict()


@pytest.fixture
def get_photo_response() -> dict[str, typing.Any]:
    return tg_methods.SendPhotoResponse.parse_obj(
        {
            'ok': True,
            'result': tg_types.Message.parse_obj({
                'chat': tg_types.Chat.parse_obj({
                    'first_name': 'TestFirstName',
                    'id': 1234567890,
                    'last_name': 'TestLastName',
                    'type': 'private',
                    'username': 'TestUserName',
                }),
                'date': 1686840262,
                'from_': tg_types.User.parse_obj({
                    'first_name': 'TestFirstName',
                    'id': 1234567890,
                    'is_bot': False,
                    'language_code': 'ru',
                    'last_name': 'TestLastName',
                    'username': 'TestUserName',
                }),
                'message_id': 12345,
                'photo': [{
                    "file_id": "BQACAgIAAxkBAAMQZJRQU7dV3gHKrckVBQk4NAoy5TsAAvw2AAJq0KlIIuX8ICpuOOwvBA",
                    "file_unique_id": "AgAD_DYAAmrQqUg",
                    "file_size": 48,
                    "width": 10,
                    "height": 10,
                }],
                "caption": "test caption",
            }),
        },
    ).dict()


@pytest.fixture
def delete_message_response() -> dict[str, typing.Any]:
    return tg_methods.DeleteMessageResponse.parse_obj({'ok': True, 'result': True}).dict()


@pytest.fixture
def keyboard() -> tg_types.InlineKeyboardMarkup:
    return tg_types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                tg_types.InlineKeyboardButton(text='button_1', callback_data='test'),
                tg_types.InlineKeyboardButton(text='button_2', callback_data='test'),
            ],
        ],
    )


@pytest.fixture
def edit_message_text_response(keyboard: tg_types.InlineKeyboardMarkup) -> dict[str, typing.Any]:
    return tg_methods.EditMessageTextResponse.parse_obj(
        {
            'ok': True,
            'result': tg_types.Message.parse_obj({
                'chat': tg_types.Chat.parse_obj({
                    'first_name': 'TestFirstName',
                    'id': 1234567890,
                    'last_name': 'TestLastName',
                    'type': 'private',
                    'username': 'TestUserName',
                }),
                'date': 1686840262,
                'from_': tg_types.User.parse_obj({
                    'first_name': 'TestFirstName',
                    'id': 1234567890,
                    'is_bot': False,
                    'language_code': 'ru',
                    'last_name': 'TestLastName',
                    'username': 'TestUserName',
                }),
                'message_id': 12345,
                'text': 'Edited text',
                'reply_markup': keyboard.dict(),
            }),
        },
    ).dict()


@pytest.fixture
def edit_message_reply_markup_response(edit_message_text_response: dict[str, typing.Any]) -> dict[str, typing.Any]:
    # unique fixture for test, but really similar to :edit_message_text_response:
    return edit_message_text_response
