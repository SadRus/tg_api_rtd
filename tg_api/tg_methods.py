import io
import json
from typing import Any, Union

from pydantic import BaseModel, Field

from .client import AsyncTgClient, SyncTgClient, TgRuntimeError, raise_for_tg_response_status
from . import tg_types


class BaseTgRequest(BaseModel, tg_types.ValidableMixin):
    """Base class representing a request to the Telegram Bot API.

    Provides utility methods for making both asynchronous and synchronous requests to the API.

    Typically used as a parent class for specific request types which include their data fields and
    possibly override or extend the base methods to customize behavior.
    """

    class Config:
        extra = 'forbid'
        validate_assignment = True
        anystr_strip_whitespace = True

    async def apost_as_json(self, api_method: str) -> bytes:
        """Send a request to the Telegram Bot API asynchronously using a JSON payload.

        :param api_method: The Telegram Bot API method to call.
        :return: The response from the Telegram Bot API as a byte string.
        """
        client = AsyncTgClient.default_client.get(None)

        if not client:
            raise TgRuntimeError('Requires AsyncTgClient to be specified before call.')

        http_response = await client.session.post(
            f'{client.api_root}{api_method}',
            headers={
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            content=self.json(exclude_none=True).encode('utf-8'),
        )
        raise_for_tg_response_status(http_response)
        return http_response.content

    def post_as_json(self, api_method: str) -> bytes:
        """Send a request to the Telegram Bot API synchronously using a JSON payload.

        :param api_method: The Telegram Bot API method to call.
        :return: The response from the Telegram Bot API as a byte string.
        """
        client = SyncTgClient.default_client.get(None)

        if not client:
            raise TgRuntimeError('Requires SyncTgClient to be specified before call.')

        http_response = client.session.post(
            f'{client.api_root}{api_method}',
            headers={
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            content=self.json(exclude_none=True).encode('utf-8'),
        )
        raise_for_tg_response_status(http_response)
        return http_response.content

    async def apost_multipart_form_data(self, api_method: str, content: dict, files: dict) -> bytes:
        """Send a request to the Telegram Bot API asynchronously using the "multipart/form-data" format.

        :param api_method: The Telegram Bot API method to call.
        :param content: A dictionary containing the content to be sent.
        :param files: A dictionary containing files to be sent.
        :return: The response from the Telegram Bot API as a byte string.
        """
        client = AsyncTgClient.default_client.get(None)

        if not client:
            raise TgRuntimeError('Requires AsyncTgClient to be specified before call.')

        if content.get('caption_entities'):
            content['caption_entities'] = json.dumps(content['caption_entities'])

        if content.get('entities'):
            content['entities'] = json.dumps(content['entities'])

        if content.get('reply_markup'):
            content['reply_markup'] = json.dumps(content['reply_markup'])

        if content.get('media'):
            content['media'] = json.dumps(content['media'])

        http_response = await client.session.post(
            f'{client.api_root}{api_method}',
            files=files,
            data=content,
        )
        raise_for_tg_response_status(http_response)
        return http_response.content

    def post_multipart_form_data(self, api_method: str, content: dict, files: dict) -> bytes:
        """Send a request to the Telegram Bot API synchronously using the "multipart/form-data" format.

        :param api_method: The Telegram Bot API method name.
        :param content: A dictionary containing the content to be sent.
        :param files: A dictionary containing files to be sent.
        :return: The response from the Telegram Bot API as a byte string.
        """
        client = SyncTgClient.default_client.get(None)

        if not client:
            raise TgRuntimeError('Requires SyncTgClient to be specified before call.')

        if content.get('caption_entities'):
            content['caption_entities'] = json.dumps(content['caption_entities'])

        if content.get('entities'):
            content['entities'] = json.dumps(content['entities'])

        if content.get('reply_markup'):
            content['reply_markup'] = json.dumps(content['reply_markup'])

        if content.get('media'):
            content['media'] = json.dumps(content['media'])

        http_response = client.session.post(
            f'{client.api_root}{api_method}',
            files=files,
            data=content,
        )
        raise_for_tg_response_status(http_response)
        return http_response.content


class BaseTgResponse(BaseModel):
    """Represents the base structure of a response from the Telegram Bot API.

    Every response from the Telegram Bot API contains certain common attributes, which are captured
    in this base model. Specific response types might extend this base structure.
    """

    ok: bool
    error_code: int | None = None
    description: str = ''

    result: Any = None

    class Config:
        extra = 'ignore'
        allow_mutation = False

    # TODO Some errors may also have an optional field 'parameters' of the type ResponseParameters, which can
    # help to automatically handle the error.


class SendMessageResponse(BaseTgResponse):
    result: tg_types.Message


class SendMessageRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `sendMessage`.

    See here https://core.telegram.org/bots/api#sendmessage
    """

    chat_id: int
    text: str = Field(min_length=1, max_length=4096)
    parse_mode: tg_types.ParseMode | None = None
    entities: list[tg_types.MessageEntity] | None = None
    disable_web_page_preview: bool | None = None
    disable_notification: bool | None = None
    protect_content: bool | None = None
    message_thread_id: bool | None = None
    allow_sending_without_reply: bool | None = None
    reply_markup: Union[
        tg_types.InlineKeyboardMarkup,
        tg_types.ReplyKeyboardMarkup,
        tg_types.ReplyKeyboardRemove,
        tg_types.ForceReply,
    ] | None = None

    class Config:
        anystr_strip_whitespace = True

    async def asend(self) -> SendMessageResponse:
        """Send HTTP request to `sendMessage` Telegram Bot API endpoint asynchronously and parse response."""
        json_payload = await self.apost_as_json('sendMessage')
        response = SendMessageResponse.parse_raw(json_payload)
        return response

    def send(self) -> SendMessageResponse:
        """Send HTTP request to `sendMessage` Telegram Bot API endpoint synchronously and parse response."""
        json_payload = self.post_as_json('sendMessage')
        response = SendMessageResponse.parse_raw(json_payload)
        return response


class SendPhotoResponse(BaseTgResponse):
    result: tg_types.Message


class SendBytesPhotoRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `sendPhoto`.

    See here https://core.telegram.org/bots/api#sendphoto
    """

    chat_id: int
    photo: bytes
    filename: str | None = None
    message_thread_id: int | None = None
    caption: str | None = Field(None, max_length=1024)
    parse_mode: str | None = None
    caption_entities: list[tg_types.MessageEntity] | None = None
    has_spoiler: bool | None = None
    disable_notification: bool | None = None
    protect_content: bool | None = None
    reply_to_message_id: int | None = None
    allow_sending_without_reply: bool | None = None
    reply_markup: Union[
        tg_types.InlineKeyboardMarkup,
        tg_types.ReplyKeyboardMarkup,
        tg_types.ReplyKeyboardRemove,
        tg_types.ForceReply,
    ] | None = None

    async def asend(self) -> SendPhotoResponse:
        """Send HTTP request to `sendPhoto` Telegram Bot API endpoint asynchronously and parse response."""
        content = self.dict(exclude_none=True, exclude={'photo'})
        photo_bytes_io = io.BytesIO(self.photo)
        photo_bytes_io.name = self.filename
        files = {'photo': photo_bytes_io}
        json_payload = await self.apost_multipart_form_data('sendPhoto', content, files)
        response = SendPhotoResponse.parse_raw(json_payload)
        return response

    def send(self) -> SendPhotoResponse:
        """Send HTTP request to `sendPhoto` Telegram Bot API endpoint synchronously and parse response."""
        content = self.dict(exclude_none=True, exclude={'photo'})
        photo_bytes_io = io.BytesIO(self.photo)
        photo_bytes_io.name = self.filename
        files = {'photo': photo_bytes_io}
        json_payload = self.post_multipart_form_data('sendPhoto', content, files)
        response = SendPhotoResponse.parse_raw(json_payload)
        return response


class SendUrlPhotoRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `sendPhoto`.

    See here https://core.telegram.org/bots/api#sendphoto
    """

    chat_id: int
    photo: str
    filename: str | None = None
    message_thread_id: int | None = None
    caption: str | None = Field(None, max_length=1024)
    parse_mode: str | None = None
    caption_entities: list[tg_types.MessageEntity] | None = None
    has_spoiler: bool | None = None
    disable_notification: bool | None = None
    protect_content: bool | None = None
    reply_to_message_id: int | None = None
    allow_sending_without_reply: bool | None = None
    reply_markup: Union[
        tg_types.InlineKeyboardMarkup,
        tg_types.ReplyKeyboardMarkup,
        tg_types.ReplyKeyboardRemove,
        tg_types.ForceReply,
    ] | None = None

    async def asend(self) -> SendPhotoResponse:
        """Send HTTP request to `sendPhoto` Telegram Bot API endpoint asynchronously and parse response."""
        json_payload = await self.apost_as_json('sendPhoto')
        response = SendPhotoResponse.parse_raw(json_payload)
        return response

    def send(self) -> SendPhotoResponse:
        """Send HTTP request to `sendPhoto` Telegram Bot API endpoint synchronously and parse response."""
        json_payload = self.post_as_json('sendPhoto')
        response = SendPhotoResponse.parse_raw(json_payload)
        return response


class SendDocumentResponse(BaseTgResponse):
    result: tg_types.Message


class SendBytesDocumentRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `sendDocument`.

    See here https://core.telegram.org/bots/api#senddocument
    """

    chat_id: int
    document: bytes
    filename: str | None = None
    message_thread_id: int | None = None
    thumbnail: bytes | str | None = None
    caption: str | None = Field(None, max_length=1024)
    parse_mode: str | None = None
    caption_entities: list[tg_types.MessageEntity] | None = None
    disable_content_type_detection: bool | None = None
    disable_notification: bool | None = None
    protect_content: bool | None = None
    reply_to_message_id: int | None = None
    allow_sending_without_reply: bool | None = None
    reply_markup: Union[
        tg_types.InlineKeyboardMarkup,
        tg_types.ReplyKeyboardMarkup,
        tg_types.ReplyKeyboardRemove,
        tg_types.ForceReply,
    ] | None = None

    async def asend(self) -> SendDocumentResponse:
        """Send HTTP request to `sendDocument` Telegram Bot API endpoint asynchronously and parse response."""
        content = self.dict(exclude_none=True, exclude={'document'})
        document_bytes = io.BytesIO(self.document)
        document_bytes.name = self.filename
        files = {'document': document_bytes}
        json_payload = await self.apost_multipart_form_data('sendDocument', content, files)
        response = SendDocumentResponse.parse_raw(json_payload)
        return response

    def send(self) -> SendDocumentResponse:
        """Send HTTP request to `sendDocument` Telegram Bot API endpoint synchronously and parse response."""
        content = self.dict(exclude_none=True, exclude={'document'})
        document_bytes = io.BytesIO(self.document)
        document_bytes.name = self.filename
        files = {'document': document_bytes}
        json_payload = self.post_multipart_form_data('sendDocument', content, files)
        response = SendDocumentResponse.parse_raw(json_payload)
        return response


class SendUrlDocumentRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `sendDocument`.

    See here https://core.telegram.org/bots/api#senddocument
    """

    chat_id: int
    document: str
    filename: str | None = None
    message_thread_id: int | None = None
    thumbnail: bytes | str | None = None
    caption: str | None = Field(None, max_length=1024)
    parse_mode: str | None = None
    caption_entities: list[tg_types.MessageEntity] | None = None
    disable_content_type_detection: bool | None = None
    disable_notification: bool | None = None
    protect_content: bool | None = None
    reply_to_message_id: int | None = None
    allow_sending_without_reply: bool | None = None
    reply_markup: Union[
        tg_types.InlineKeyboardMarkup,
        tg_types.ReplyKeyboardMarkup,
        tg_types.ReplyKeyboardRemove,
        tg_types.ForceReply,
    ] | None = None

    async def asend(self) -> SendDocumentResponse:
        """Send HTTP request to `sendDocument` Telegram Bot API endpoint asynchronously and parse response."""
        json_payload = await self.apost_as_json('sendDocument')
        response = SendDocumentResponse.parse_raw(json_payload)
        return response

    def send(self) -> SendDocumentResponse:
        """Send HTTP request to `sendDocument` Telegram Bot API endpoint synchronously and parse response."""
        json_payload = self.post_as_json('sendDocument')
        response = SendDocumentResponse.parse_raw(json_payload)
        return response


class DeleteMessageResponse(BaseTgResponse):
    result: bool


class DeleteMessageRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `deleteMessage`.

    See here https://core.telegram.org/bots/api#deletemessage
    """

    chat_id: int
    message_id: int

    async def asend(self) -> DeleteMessageResponse:
        """Send HTTP request to `deleteMessage` Telegram Bot API endpoint asynchronously and parse response."""
        json_payload = await self.apost_as_json('deleteMessage')
        response = DeleteMessageResponse.parse_raw(json_payload)
        return response

    def send(self) -> DeleteMessageResponse:
        """Send HTTP request to `deleteMessage` Telegram Bot API endpoint synchronously and parse response."""
        json_payload = self.post_as_json('deleteMessage')
        response = DeleteMessageResponse.parse_raw(json_payload)
        return response


class EditMessageTextResponse(BaseTgResponse):
    result: tg_types.Message | bool


class EditMessageTextRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `editMessageText`.

    See here https://core.telegram.org/bots/api#editmessagetext
    """

    chat_id: int | None = None
    message_id: int | None = None
    inline_message_id: str | None = None
    text: str = Field(min_length=1, max_length=4096)
    parse_mode: str | None = None
    entities: list[tg_types.MessageEntity] | None = None
    disable_web_page_preview: bool | None = None
    reply_markup: tg_types.InlineKeyboardMarkup | None = None

    async def asend(self) -> EditMessageTextResponse:
        """Send HTTP request to `editmessagetext` Telegram Bot API endpoint asynchronously and parse response."""
        json_payload = await self.apost_as_json('editmessagetext')
        response = EditMessageTextResponse.parse_raw(json_payload)
        return response

    def send(self) -> EditMessageTextResponse:
        """Send HTTP request to `editmessagetext` Telegram Bot API endpoint synchronously and parse response."""
        json_payload = self.post_as_json('editmessagetext')
        response = EditMessageTextResponse.parse_raw(json_payload)
        return response


class EditMessageReplyMarkupResponse(BaseTgResponse):
    result: tg_types.Message | bool


class EditMessageReplyMarkupRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `editMessageReplyMarkup`.

    See here https://core.telegram.org/bots/api#editmessagereplymarkup
    """

    chat_id: int | None = None
    message_id: int | None = None
    inline_message_id: str | None = None
    reply_markup: tg_types.InlineKeyboardMarkup | None = None

    async def asend(self) -> EditMessageReplyMarkupResponse:
        """Send HTTP request to `editmessagereplymarkup` Telegram Bot API endpoint asynchronously and parse response."""
        json_payload = await self.apost_as_json('editmessagereplymarkup')
        response = EditMessageReplyMarkupResponse.parse_raw(json_payload)
        return response

    def send(self) -> EditMessageReplyMarkupResponse:
        """Send HTTP request to `editmessagereplymarkup` Telegram Bot API endpoint synchronously and parse response."""
        json_payload = self.post_as_json('editmessagereplymarkup')
        response = EditMessageReplyMarkupResponse.parse_raw(json_payload)
        return response


class EditMessageCaptionResponse(BaseTgResponse):
    result: tg_types.Message | bool


class EditMessageCaptionRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `editMessageCaption`.

    See here https://core.telegram.org/bots/api#editmessagecaption
    """

    chat_id: int | None = None
    message_id: int | None = None
    inline_message_id: str | None = None
    caption: str | None = Field(None, max_length=1024)
    parse_mode: str | None = None
    caption_entities: list[tg_types.MessageEntity] | None = None
    reply_markup: tg_types.InlineKeyboardMarkup | None = None

    async def asend(self) -> EditMessageCaptionResponse:
        """Send HTTP request to `editmessagecaption` Telegram Bot API endpoint asynchronously and parse response."""
        json_payload = await self.apost_as_json('editmessagecaption')
        response = EditMessageCaptionResponse.parse_raw(json_payload)
        return response

    def send(self) -> EditMessageCaptionResponse:
        """Send HTTP request to `editmessagecaption` Telegram Bot API endpoint synchronously and parse response."""
        json_payload = self.post_as_json('editmessagecaption')
        response = EditMessageCaptionResponse.parse_raw(json_payload)
        return response


class EditMessageMediaResponse(BaseTgResponse):
    result: tg_types.Message | bool


class EditBytesMessageMediaRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `editmessagemedia`.

    See here https://core.telegram.org/bots/api#editmessagemedia
    """

    chat_id: int | None = None
    message_id: int | None = None
    inline_message_id: str | None = None
    media: Union[tg_types.InputMediaBytesDocument, tg_types.InputMediaBytesPhoto]
    reply_markup: tg_types.InlineKeyboardMarkup | None = None

    async def asend(self) -> EditMessageMediaResponse:
        """Send HTTP request to `editmessagemedia` Telegram Bot API endpoint asynchronously and parse response."""
        content = self.dict(exclude_none=True)

        content['media'].pop('media_content')
        media_bytes = io.BytesIO(self.media.media_content)
        files = {self.media.media: media_bytes}

        if not self.media.media.startswith('attach://'):
            content['media']['media'] = f"attach://{content['media']['media']}"

        if content['media'].get('thumbnail') and content['media'].get('thumbnail_content'):
            thumbnail = content['media']['thumbnail']
            thumbnail_content = content['media'].pop('thumbnail_content')
            thumbnail_bytes = io.BytesIO(thumbnail_content)
            files[thumbnail] = thumbnail_bytes

            if not thumbnail.startswith('attach://'):
                content['media']['thumbnail'] = f"attach://{thumbnail}"

        json_payload = await self.apost_multipart_form_data('editmessagemedia', content, files)
        response = EditMessageMediaResponse.parse_raw(json_payload)
        return response

    def send(self) -> EditMessageMediaResponse:
        """Send HTTP request to `editmessagemedia` Telegram Bot API endpoint synchronously and parse response."""
        content = self.dict(exclude_none=True)

        content['media'].pop('media_content')
        media_bytes = io.BytesIO(self.media.media_content)
        files = {self.media.media: media_bytes}

        if not self.media.media.startswith('attach://'):
            content['media']['media'] = f"attach://{content['media']['media']}"

        if content['media'].get('thumbnail') and content['media'].get('thumbnail_content'):
            thumbnail = content['media']['thumbnail']
            thumbnail_content = content['media'].pop('thumbnail_content')
            thumbnail_bytes = io.BytesIO(thumbnail_content)
            files[thumbnail] = thumbnail_bytes

            if not thumbnail.startswith('attach://'):
                content['media']['thumbnail'] = f"attach://{thumbnail}"

        json_payload = self.post_multipart_form_data('editmessagemedia', content, files)
        response = EditMessageMediaResponse.parse_raw(json_payload)
        return response


class EditUrlMessageMediaRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `editmessagemedia`.

    See here https://core.telegram.org/bots/api#editmessagemedia
    """

    chat_id: int | None = None
    message_id: int | None = None
    inline_message_id: str | None = None
    media: Union[tg_types.InputMediaUrlDocument, tg_types.InputMediaUrlPhoto]
    reply_markup: tg_types.InlineKeyboardMarkup | None = None

    async def asend(self) -> EditMessageMediaResponse:
        """Send HTTP request to `editmessagemedia` Telegram Bot API endpoint asynchronously and parse response."""
        json_payload = await self.apost_as_json('editmessagemedia')
        response = EditMessageMediaResponse.parse_raw(json_payload)
        return response

    def send(self) -> EditMessageMediaResponse:
        """Send HTTP request to `editmessagemedia` Telegram Bot API endpoint synchronously and parse response."""
        json_payload = self.post_as_json('editmessagemedia')
        response = EditMessageMediaResponse.parse_raw(json_payload)
        return response
