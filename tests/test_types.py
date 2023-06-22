from tg_api import tg_types


def test_update_parsing():
    raw_payload = b'''
        {
            "update_id":692509117,
            "message": {
                "message_id":3033,
                "from": {
                    "id":43434343,
                    "is_bot":false,
                    "first_name":"\\u0415\\u0432\\u0433\\u0435\\u043d\\u0438\\u0439",
                    "last_name":"",
                    "username":"anonymous",
                    "language_code":"en"
                },
                "chat": {
                    "id":43434343,
                    "first_name":"\\u0415\\u0432\\u0433\\u0435\\u043d\\u0438\\u0439",
                    "last_name":"",
                    "username":"anonymous",
                    "type":"private"
                },
                "date":1686903532,
                "text":"/start",
                "entities": [
                    {"offset":0, "length":6, "type":"bot_command"}
                ]
            }
        }
    '''
    tg_types.Update.parse_raw(raw_payload)


class TestMessageParsing:
    def test_text_message(self):
        raw_payload = b'''
        {
            "message_id":3033,
            "from": {
                "id":43434343,
                "is_bot":false,
                "first_name":"\\u0415\\u0432\\u0433\\u0435\\u043d\\u0438\\u0439",
                "last_name":"",
                "username":"anonymous",
                "language_code":"en"
            },
            "chat": {
                "id":43434343,
                "first_name":"\\u0415\\u0432\\u0433\\u0435\\u043d\\u0438\\u0439",
                "last_name":"",
                "username":"anonymous",
                "type":"private"
            },
            "date":1686903532,
            "text":"/start",
            "entities": [
                {"offset":0, "length":6, "type":"bot_command"}
            ]
        }
        '''
        message = tg_types.Message.parse_raw(raw_payload)
        assert message.text == "/start"
        assert isinstance(message.from_, tg_types.User)
        assert message.from_.id == 43434343
        assert isinstance(message.chat, tg_types.Chat)
        assert message.chat.id == 43434343
        assert message.reply_to_message is None

    def test_message_with_document(self):
        raw_payload = b'''
        {
            "message_id": 16,
            "from": {
                "id":43434343,
                "is_bot":false,
                "first_name":"\\u0415\\u0432\\u0433\\u0435\\u043d\\u0438\\u0439",
                "last_name":"",
                "username":"anonymous",
                "language_code":"en"
            },
            "chat": {
                "id":43434343,
                "first_name":"\\u0415\\u0432\\u0433\\u0435\\u043d\\u0438\\u0439",
                "last_name":"",
                "username":"anonymous",
                "type":"private"
            },
            "date": 1687441491,
            "document": {
                "file_name": "document.csv",
                "mime_type": "text/csv",
                "file_id": "BQACAgIAAxkBAAMQZJRQU7dV3gHKrckVBQk4NAoy5TsAAvw2AAJq0KlIIuX8ICpuOOwvBA",
                "file_unique_id": "AgAD_DYAAmrQqUg",
                "file_size": 48
            },
            "caption": "test caption"
        }
        '''
        message = tg_types.Message.parse_raw(raw_payload)
        assert message.text is None
        assert message.caption == "test caption"
        assert isinstance(message.from_, tg_types.User)
        assert message.from_.id == 43434343
        assert isinstance(message.chat, tg_types.Chat)
        assert message.chat.id == 43434343
        assert isinstance(message.document, dict)
        assert message.document['file_id'] == "BQACAgIAAxkBAAMQZJRQU7dV3gHKrckVBQk4NAoy5TsAAvw2AAJq0KlIIuX8ICpuOOwvBA"

    def test_message_keyboard_click(self):
        raw_payload = b'''
        {
            "message_id": 20,
            "from": {
                "id": 6202114561,
                "is_bot": true,
                "first_name": "bot name",
                "username": "username_bot"
            },
            "chat": {
                "id":43434343,
                "first_name":"\\u0415\\u0432\\u0433\\u0435\\u043d\\u0438\\u0439",
                "last_name":"",
                "username":"anonymous",
                "type":"private"
            },
            "date": 1687442983,
            "text": "Text under keyboard",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {
                            "text": "button_1",
                            "callback_data": "test1"
                        },
                        {
                            "text": "button_2",
                            "callback_data": "test2"
                        }
                    ]
                ]
            }
        }
        '''
        message = tg_types.Message.parse_raw(raw_payload)
        assert message.text == "Text under keyboard"
        assert isinstance(message.from_, tg_types.User)
        assert message.from_.id == 6202114561
        assert isinstance(message.chat, tg_types.Chat)
        assert message.chat.id == 43434343
        assert isinstance(message.reply_markup, tg_types.InlineKeyboardMarkup)
        assert len(message.reply_markup.inline_keyboard) == 1
        assert len(message.reply_markup.inline_keyboard[0]) == 2