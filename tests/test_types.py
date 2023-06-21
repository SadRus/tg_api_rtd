from tg_api.tg_types import Update


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
    Update.parse_raw(raw_payload)
