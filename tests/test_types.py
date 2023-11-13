from tg_api import tg_types


def test_inline_query_parsing() -> None:
    payload = {
        "id": "unique",
        "from": {
            "id": 43434343,
            "is_bot": False,
            "first_name": "\\u0415\\u0432\\u0433\\u0435\\u043d\\u0438\\u0439",
            "last_name": "",
            "username": "anonymous",
            "language_code": "en",
        },
        "query": "query",
        "offset": "offset",
        "chat_type": "chat_type",
        "location": {
            "longitude": 1.234,
            "latitude": 1.345,
            "horizontal_accuracy": 1.456,
            "live_period": 1,
            "heading": 2,
            "proximity_alert_radius": 3,
        },
    }

    inline_query = tg_types.InlineQuery.parse_obj(payload)

    assert inline_query.id == 'unique'
    assert isinstance(inline_query.from_, tg_types.User)
    assert inline_query.from_.username == 'anonymous'
    assert inline_query.query == 'query'
    assert inline_query.offset == 'offset'
    assert inline_query.chat_type == 'chat_type'
    assert isinstance(inline_query.location, tg_types.Location)
    assert inline_query.location.longitude == 1.234
    assert inline_query.location.latitude == 1.345
    assert inline_query.location.horizontal_accuracy == 1.456
    assert inline_query.location.live_period == 1
    assert inline_query.location.heading == 2
    assert inline_query.location.proximity_alert_radius == 3


def test_update_parsing() -> None:
    payload = {
        "update_id": 692509117,
        "message": {
            "message_id": 3033,
            "from": {
                "id": 43434343,
                "is_bot": False,
                "first_name": "\\u0415\\u0432\\u0433\\u0435\\u043d\\u0438\\u0439",
                "last_name": "",
                "username": "anonymous",
                "language_code": "en",
            },
            "chat": {
                "id": 43434343,
                "first_name": "\\u0415\\u0432\\u0433\\u0435\\u043d\\u0438\\u0439",
                "last_name": "",
                "username": "anonymous",
                "type": "private",
            },
            "date": 1686903532,
            "text": "/start",
            "entities": [
                {"offset": 0, "length": 6, "type": "bot_command"},
            ],
        },
    }
    tg_types.Update.parse_obj(payload)


class TestMessageParsing:
    def test_text_message(self) -> None:
        payload = {
            "message_id": 3033,
            "from": {
                "id": 43434343,
                "is_bot": False,
                "first_name": "\\u0415\\u0432\\u0433\\u0435\\u043d\\u0438\\u0439",
                "last_name": "",
                "username": "anonymous",
                "language_code": "en",
            },
            "chat": {
                "id": 43434343,
                "first_name": "\\u0415\\u0432\\u0433\\u0435\\u043d\\u0438\\u0439",
                "last_name": "",
                "username": "anonymous",
                "type": "private",
            },
            "date": 1686903532,
            "text": "/start",
            "entities": [
                {"offset": 0, "length": 6, "type": "bot_command"},
            ],
        }

        message = tg_types.Message.parse_obj(payload)
        assert message.text == "/start"
        assert isinstance(message.from_, tg_types.User)
        assert message.from_.id == 43434343
        assert isinstance(message.chat, tg_types.Chat)
        assert message.chat.id == 43434343
        assert message.reply_to_message is None

    def test_message_with_document(self) -> None:
        payload = {
            "message_id": 16,
            "from": {
                "id": 43434343,
                "is_bot": False,
                "first_name": "\\u0415\\u0432\\u0433\\u0435\\u043d\\u0438\\u0439",
                "last_name": "",
                "username": "anonymous",
                "language_code": "en",
            },
            "chat": {
                "id": 43434343,
                "first_name": "\\u0415\\u0432\\u0433\\u0435\\u043d\\u0438\\u0439",
                "last_name": "",
                "username": "anonymous",
                "type": "private",
            },
            "date": 1687441491,
            "document": {
                "file_name": "document.csv",
                "mime_type": "text/csv",
                "file_id": "BQACAgIAAxkBAAMQZJRQU7dV3gHKrckVBQk4NAoy5TsAAvw2AAJq0KlIIuX8ICpuOOwvBA",
                "file_unique_id": "AgAD_DYAAmrQqUg",
                "file_size": 48,
            },
            "caption": "test caption",
        }

        message = tg_types.Message.parse_obj(payload)
        assert message.text is None
        assert message.caption == "test caption"
        assert isinstance(message.from_, tg_types.User)
        assert message.from_.id == 43434343
        assert isinstance(message.chat, tg_types.Chat)
        assert message.chat.id == 43434343
        assert isinstance(message.document, dict)
        assert message.document['file_id'] == "BQACAgIAAxkBAAMQZJRQU7dV3gHKrckVBQk4NAoy5TsAAvw2AAJq0KlIIuX8ICpuOOwvBA"

    def test_message_keyboard_click(self) -> None:
        raw_payload = {
            "message_id": 20,
            "from": {
                "id": 6202114561,
                "is_bot": True,
                "first_name": "bot name",
                "username": "username_bot",
            },
            "chat": {
                "id": 43434343,
                "first_name": "\\u0415\\u0432\\u0433\\u0435\\u043d\\u0438\\u0439",
                "last_name": "",
                "username": "anonymous",
                "type": "private",
            },
            "date": 1687442983,
            "text": "Text under keyboard",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {
                            "text": "button_1",
                            "callback_data": "test1",
                        },
                        {
                            "text": "button_2",
                            "callback_data": "test2",
                        },
                    ],
                ],
            },
        }

        message = tg_types.Message.parse_obj(raw_payload)
        assert message.text == "Text under keyboard"
        assert isinstance(message.from_, tg_types.User)
        assert message.from_.id == 6202114561
        assert isinstance(message.chat, tg_types.Chat)
        assert message.chat.id == 43434343
        assert isinstance(message.reply_markup, tg_types.InlineKeyboardMarkup)
        assert len(message.reply_markup.inline_keyboard) == 1
        assert len(message.reply_markup.inline_keyboard[0]) == 2


def test_update_message() -> None:
    payload = {
        "update_id": 815922528,
        "message": {
            "message_id": 194,
            "from": {
                "id": 305151544,
                "is_bot": False,
                "first_name": "\\u041d\\u0438\\u043a\\u0438\\u0442\\u0430",
                "username": "UsernameTest",
                "language_code": "ru",
            },
            "chat": {
                "id": 305151544,
                "first_name": "\\u041d\\u0438\\u043a\\u0438\\u0442\\u0430",
                "username": "UsernameTest",
                "type": "private",
            },
            "date": 1687434741,
            "text": "test text",
        },
    }
    update_obj = tg_types.Update.parse_obj(payload)
    assert isinstance(update_obj, tg_types.Update)
    assert update_obj.message
    assert update_obj.message.message_id == 194
    assert isinstance(update_obj.message.from_, tg_types.User)
    assert isinstance(update_obj.message.chat, tg_types.Chat)
    assert update_obj.message.chat.id == 305151544
    assert update_obj.message.text == "test text"


def test_update_file() -> None:
    payload = {
        "update_id": 815922511,
        "message": {
            "message_id": 150,
            "from": {
                "id": 305151544,
                "is_bot": False,
                "first_name": "\\u041d\\u0438\\u043a\\u0438\\u0442\\u0430",
                "username": "UsernameTest",
                "language_code": "ru",
            },
            "chat": {
                "id": 305151544,
                "first_name": "\\u041d\\u0438\\u043a\\u0438\\u0442\\u0430",
                "username": "UsernameTest",
                "type": "private",
            },
            "date": 1687382943,
            "document": {
                "file_name": "\\u043d\\u044b\\u0439 \\u0434\\u043e\\u043a\\u0443\\u043c\\u0435\\u043d\\u0442 1",
                "mime_type": "text/plain",
                "file_id": "BQACAgIAAxkBAAOWZJNrn6fnltGx65eSxok3r3Q2qGMAAoo4AAISLJlILYF9HWhc_aMvBA",
                "file_unique_id": "AgADijgAAhIsmUg",
                "file_size": 63,
            },
        },
    }
    update_obj = tg_types.Update.parse_obj(payload)
    assert isinstance(update_obj, tg_types.Update)
    assert update_obj.message
    assert update_obj.message.message_id == 150
    assert isinstance(update_obj.message.chat, tg_types.Chat)
    assert update_obj.message.chat.id == 305151544
    assert update_obj.message.document
    assert update_obj.message.document['file_id'] == "BQACAgIAAxkBAAOWZJNrn6fnltGx65eSxok3r3Q2qGMAAoo4AAISLJlI" \
        "LYF9HWhc_aMvBA"
    assert update_obj.message.document['file_name'] == "\\u043d\\u044b\\u0439 " \
        "\\u0434\\u043e\\u043a\\u0443\\u043c\\u0435\\u043d\\u0442 1"


def test_update_btn() -> None:
    payload = {
        "update_id": 815922533,
        "callback_query": {
            "id": "1310616028335436612",
            "from": {
                "id": 305151544,
                "is_bot": False,
                "first_name": "\\u041d\\u0438\\u043a\\u0438\\u0442\\u0430",
                "username": "UsernameTest",
                "language_code": "ru",
            },
            "message": {
                "message_id": 202,
                "from": {
                    "id": 6235267584,
                    "is_bot": True,
                    "first_name": "tgapi zusmanone",
                    "username": "tgapizusman_bot",
                },
                "chat": {
                    "id": 305151544,
                    "first_name": "\\u041d\\u0438\\u043a\\u0438\\u0442\\u0430",
                    "username": "UsernameTest",
                    "type": "private",
                },
                "date": 1687437107,
                "text": "Message proofs keyboard support.",
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {"text": "button_1", "callback_data": "test"},
                            {"text": "button_2", "callback_data": "test"},
                        ],
                    ],
                },
            },
            "inline_message_id": "12345",
            "chat_instance": "-9009133691020524056",
            "data": "test",
        },
    }
    update_obj = tg_types.Update.parse_obj(payload)
    assert isinstance(update_obj, tg_types.Update)
    assert isinstance(update_obj.callback_query, tg_types.CallbackQuery)
    assert update_obj.callback_query
    assert update_obj.callback_query.message
    assert isinstance(update_obj.callback_query.message.chat, tg_types.Chat)
    assert update_obj.callback_query.message.chat.id == 305151544
    assert isinstance(update_obj.callback_query.message.reply_markup, tg_types.InlineKeyboardMarkup)
    assert update_obj.callback_query.message.reply_markup.inline_keyboard[0][0].text == 'button_1'
    assert update_obj.callback_query.inline_message_id == "12345"
