from __future__ import annotations

from textwrap import dedent
from enum import Enum
from typing import Any, Union, Optional

from pydantic import BaseModel, AnyHttpUrl, Field


class ParseMode(str, Enum):
    MarkdownV2 = 'MarkdownV2'  # https://core.telegram.org/bots/api#markdownv2-style
    HTML = 'HTML'  # https://core.telegram.org/bots/api#html-style
    Markdown = 'Markdown'  # legacy mode https://core.telegram.org/bots/api#markdown-style


class User(BaseModel):
    """This model represents a Telegram user or bot.

    See here: https://core.telegram.org/bots/api#user
    """

    id: int = Field( # noqa A003
        description=dedent("""\
            Unique identifier for this user or bot. This number may have more than 32 significant bits and
            some programming languages may have difficulty/silent defects in interpreting it.
            But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are
            safe for storing this identifier.
        """),
    )
    is_bot: bool = Field(
        description="True, if this user is a bot.",
    )
    first_name: str = Field(
        description="User's or bot's first name.",
    )
    last_name: str | None = Field(
        default=None,
        description="Optional. User's or bot's last name.",
    )
    username: str | None = Field(
        default=None,
        description="Optional. User's or bot's username.",
    )
    language_code: str | None = Field(
        default=None,
        description="Optional. IETF language tag of the user's language.",
    )
    is_premium: bool | None = Field(
        default=None,
        description="Optional. True, if this user is a Telegram Premium user.",
    )
    added_to_attachment_menu: bool | None = Field(
        default=None,
        description="Optional. True, if this user added the bot to the attachment menu.",
    )
    can_join_groups: bool | None = Field(
        default=None,
        description="Optional. True, if the bot can be invited to groups. Returned only in getMe.",
    )
    can_read_all_group_messages: bool | None = Field(
        default=None,
        description="Optional. True, if privacy mode is disabled for the bot. Returned only in getMe.",
    )
    supports_inline_queries: bool | None = Field(
        default=None,
        description="Optional. True, if the bot supports inline queries. Returned only in getMe.",
    )


class Chat(BaseModel):
    """This model represents a chat.

    See here: https://core.telegram.org/bots/api#chat
    """

    id: int = Field( # noqa A003
        description=dedent("""\
            Unique identifier for this chat. This number may have more than 32 significant bits and some programming
            languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits,
            so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
        """),
    )
    type: str = Field( # noqa A003
        description="Type of chat, can be either “private”, “group”, “supergroup” or “channel”.",
    )
    title: str | None = Field(
        default=None,
        description="Optional. Title, for supergroups, channels and group chats.",
    )
    username: str | None = Field(
        default=None,
        description="Optional. Username, for private chats, supergroups and channels if available.",
    )
    first_name: str | None = Field(
        default=None,
        description="Optional. First name of the other party in a private chat.",
    )
    last_name: str | None = Field(
        default=None,
        description="Optional. Last name of the other party in a private chat.",
    )
    is_forum: bool | None = Field(
        default=None,
        description="Optional. True, if the supergroup chat is a forum (has topics enabled).",
    )
    photo: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Chat photo. Returned only in getChat.",
    )
    active_usernames: list[str] | None = Field(
        default=None,
        description=dedent("""\
            Optional. If non-empty, the list of all active chat usernames;
            for private chats, supergroups and channels. Returned only in getChat.
        """),
    )
    emoji_status_custom_emoji_id: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. Custom emoji identifier of emoji status of the other party in a private chat.
            Returned only in getChat.
        """),
    )
    bio: str | None = Field(
        default=None,
        description="Optional. Bio of the other party in a private chat. Returned only in getChat.",
    )
    has_private_forwards: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. True, if privacy settings of the other party in the private chat allows
            to use tg://user?id=<user_id> links only in chats with the user. Returned only in getChat.
        """),
    )
    has_restricted_voice_and_video_messages: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. True, if the privacy settings of the other party restrict sending
            voice and video note messages in the private chat. Returned only in getChat.
        """),
    )
    join_to_send_messages: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. True, if users need to join the supergroup before they can send messages.
            Returned only in getChat.
        """),
    )
    join_by_request: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. True, if all users directly joining the supergroup need
            to be approved by supergroup administrators. Returned only in getChat.
        """),
    )
    description: str | None = Field(
        default=None,
        description="Optional. Description, for groups, supergroups and channel chats. Returned only in getChat.",
    )
    invite_link: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. Primary invite link, for groups, supergroups and channel chats. Returned only in getChat.
        """),
    )
    pinned_message: Message | None = Field(
        default=None,
        description="Optional. The most recent pinned message (by sending date). Returned only in getChat.",
    )
    permissions: dict[str, Any] | None = Field(
        default=None,
        description=dedent("""\
            Optional. Default chat member permissions, for groups and supergroups. Returned only in getChat.
        """),
    )
    slow_mode_delay: int | None = Field(
        default=None,
        description=dedent("""\
            Optional. For supergroups, the minimum allowed delay between consecutive messages sent
            by each unpriviledged user; in seconds. Returned only in getChat.
        """),
    )
    message_auto_delete_time: int | None = Field(
        default=None,
        description=dedent("""\
            Optional. The time after which all messages sent to the chat will be automatically deleted; in seconds.
            Returned only in getChat.
        """),
    )
    has_aggressive_anti_spam_enabled: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. True, if aggressive anti-spam checks are enabled in the supergroup.
            The field is only available to chat administrators. Returned only in getChat.
        """),
    )
    has_hidden_members: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. True, if non-administrators can only get the list of bots and administrators in the chat.
            Returned only in getChat.
        """),
    )
    has_protected_content: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. True, if messages from the chat can't be forwarded to other chats. Returned only in getChat.
        """),
    )
    sticker_set_name: str | None = Field(
        default=None,
        description="Optional. For supergroups, name of group sticker set. Returned only in getChat.",
    )
    can_set_sticker_set: bool | None = Field(
        default=None,
        description="Optional. True, if the bot can change the group sticker set. Returned only in getChat.",
    )
    linked_chat_id: int | None = Field(
        default=None,
        description=dedent("""\
            Optional. Unique identifier for the linked chat, i.e. the discussion group identifier for
            a channel and vice versa;for supergroups and channel chats. This identifier may be greater
            than 32 bits and some programming languages may have difficulty/silent defects in interpreting it.
            But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float type are safe
            for storing this identifier. Returned only in getChat.
        """),
    )


class KeyboardButton(BaseModel):
    """This model represents one button of the reply keyboard.

    For simple text buttons, String can be used instead of this object to specify the button text.
    The optional fields web_app, request_user, request_chat, request_contact,
    request_location, and request_poll are mutually exclusive.

    See here: https://core.telegram.org/bots/api#keyboardbutton
    """

    text: str = Field(
        description=dedent("""\
            Text of the button. If none of the optional fields are used, it will be sent
            as a message when the button is pressed
        """),
    )
    request_user: dict[str, Union[int, bool]] | None = Field(
        default=None,
        description=dedent("""\
            Optional. If specified, pressing the button will open a list of suitable users.
            Tapping on any user will send their identifier to the bot in a “user_shared” service message.
            Available in private chats only.
        """),
    )
    request_chat: dict[str, Union[int, bool, dict[str, bool]]] | None = Field(
        default=None,
        description=dedent("""\
            Optional. If specified, pressing the button will open a list of suitable chats.
            Tapping on a chat will send its identifier to the bot in a “chat_shared” service message.
            Available in private chats only.
        """),
    )
    request_contact: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. If True, the user's phone number will be sent as a contact when the button is pressed.
            Available in private chats only.
        """),
    )
    request_location: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. If True, the user's current location will be sent when the button is pressed.
            Available in private chats only.
        """),
    )
    request_poll: dict[str, str] | None = Field(
        default=None,
        description=dedent("""\
            Optional. If specified, the user will be asked to create a poll and send it to the bot when
            the button is pressed. Available in private chats only.
        """),
    )
    web_app: dict[str, AnyHttpUrl] | None = Field(
        default=None,
        description=dedent("""\
            Optional. If specified, the described Web App will be launched when the button is pressed.
            The Web App will be able to send a “web_app_data” service message. Available in private chats only.
        """),
    )


class ReplyKeyboardMarkup(BaseModel):
    """This model represents a custom keyboard with reply options.

    See here: https://core.telegram.org/bots/api#replykeyboardmarkup
    """

    keyboard: list[list[KeyboardButton]] = Field(
        description="Array of button rows, each represented by an Array of KeyboardButton objects",
    )
    is_persistent: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. Requests clients to always show the keyboard when the regular keyboard is hidden.
            Defaults to false, in which case the custom keyboard can be hidden and opened with a keyboard icon.
        """),
    )
    resize_keyboard: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. Requests clients to resize the keyboard vertically for optimal
            fit (e.g., make the keyboard smaller if there are just two rows of buttons).
            Defaults to false, in which case the custom keyboard is always
            of the same height as the app's standard keyboard.
        """),
    )
    one_time_keyboard: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. Requests clients to hide the keyboard as soon as it's been used.
            The keyboard will still be available, but clients will automatically display
            the usual letter-keyboard in the chat - the user can press a special button
            in the input field to see the custom keyboard again. Defaults to false.
        """),
    )
    input_field_placeholder: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. The placeholder to be shown in the input field when the keyboard is active; 1-64 characters.
        """),
    )
    selective: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. Use this parameter if you want to show the keyboard to specific users only.
            Targets:
            1) users that are @mentioned in the text of the Message object;
            2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.
            Example:
            A user requests to change the bot's language, bot replies to the request with a keyboard to
            select the new language. Other users in the group don't see the keyboard.
        """),
    )


class ReplyKeyboardRemove(BaseModel):
    """Upon receiving a message with this object, Telegram clients will remove the current.

    custom keyboard and display the default letter-keyboard. By default, custom keyboards
    are displayed until a new keyboard is sent by a bot. An exception is made for one-time
    keyboards that are hidden immediately after the user presses a button

    See here: https://core.telegram.org/bots/api#replykeyboardremove
    """

    remove_keyboard: bool = Field(
        description=dedent("""\
            Requests clients to remove the custom keyboard (user will not be able to summon this keyboard;
            if you want to hide the keyboard from sight but keep it accessible,
            use one_time_keyboard in ReplyKeyboardMarkup).
        """),
    )
    selective: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. Use this parameter if you want to remove the keyboard for specific users only.
            Targets:
            1) users that are @mentioned in the text of the Message object;
            2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.
            Example:
            A user votes in a poll, bot returns confirmation message in reply to the vote and removes
            the keyboard for that user, while still showing the keyboard with poll
            options to users who haven't voted yet.
        """),
    )


class ForceReply(BaseModel):
    """Upon receiving a message with this object, Telegram clients will display a reply.

    interface to the user (act as if the user has selected the bot's message and tapped 'Reply').
    This can be extremely useful if you want to create user-friendly step-by-step interfaces
    without having to sacrifice privacy mode.

    See here: https://core.telegram.org/bots/api#forcereply
    """

    force_reply: bool = Field(
        description=dedent("""\
            Shows reply interface to the user, as if they manually selected the bot's message and tapped 'Reply'.
        """),
    )
    input_field_placeholder: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. The placeholder to be shown in the input field when the reply is active; 1-64 characters.
        """),
    )
    selective: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. Use this parameter if you want to force reply from specific users only.
            Targets:
            1) users that are @mentioned in the text of the Message object;
            2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.
        """),
    )


class InlineKeyboardButton(BaseModel):
    """This model represents one button of an inline keyboard.

    See here: https://core.telegram.org/bots/api#inlinekeyboardbutton
    """

    text: str = Field(
        description="Label text on the button",
    )
    url: str | None = Field(
        default=None,
        description="Optional. HTTP or tg:// URL to be opened when the button is pressed. Links tg://user?id=<user_id> can be used to mention a user by their ID without using a username, if this is allowed by their privacy settings.",
    )
    callback_data: str | None = Field(
        default=None,
        description="Optional. Data to be sent in a callback query to the bot when button is pressed, 1-64 bytes",
    )
    web_app: dict[str, AnyHttpUrl] | None = Field(
        default=None,
        description="Optional. Description of the Web App that will be launched when the user presses the button. The Web App will be able to send an arbitrary message on behalf of the user using the method answerWebAppQuery. Available only in private chats between a user and the bot.",
    )
    login_url: dict[str, Union[str, bool]] | None = Field(
        default=None,
        description="Optional. An HTTPS URL used to automatically authorize the user. Can be used as a replacement for the Telegram Login Widget.",
    )
    switch_inline_query: str | None = Field(
        default=None,
        description="Optional. If set, pressing the button will prompt the user to select one of their chats, open that chat and insert the bot's username and the specified inline query in the input field. May be empty, in which case just the bot's username will be inserted.",
    )
    switch_inline_query_current_chat: str | None = Field(
        default=None,
        description="Optional. If set, pressing the button will insert the bot's username and the specified inline query in the current chat's input field. May be empty, in which case only the bot's username will be inserted. This offers a quick way for the user to open your bot in inline mode in the same chat - good for selecting something from multiple options.",
    )
    switch_inline_query_chosen_chat: dict[str, Union[str, bool]] | None = Field(
        default=None,
        description="Optional. If set, pressing the button will prompt the user to select one of their chats of the specified type, open that chat and insert the bot's username and the specified inline query in the input field",
    )
    callback_game: Any | None = Field(
        default=None,
        description="Optional. Description of the game that will be launched when the user presses the button. NOTE: This type of button must always be the first button in the first row.",
    )
    pay: bool | None = Field(
        default=None,
        description="Optional. Specify True, to send a Pay button. NOTE: This type of button must always be the first button in the first row and can only be used in invoice messages.",
    )


class InlineKeyboardMarkup(BaseModel):
    """This model represents an inline keyboard that appears right next to the message it belongs to.

    See here: https://core.telegram.org/bots/api#inlinekeyboardmarkup
    """

    inline_keyboard: list[list[InlineKeyboardButton]] = Field(
        description="Array of button rows, each represented by an Array of InlineKeyboardButton objects",
    )


class Invoice(BaseModel):
    """This model contains basic information about an invoice.

    See here: https://core.telegram.org/bots/api#invoice
    """

    title: str = Field(
        description="Product name",
    )
    description: str = Field(
        description="Product description",
    )
    start_parameter: str = Field(
        description="Unique bot deep-linking parameter that can be used to generate this invoice",
    )
    currency: str = Field(
        description="Three-letter ISO 4217 currency code",
    )
    total_amount: int = Field(
        description="Total price in the smallest units of the currency (integer, not float/double)",
    )


class ShippingAddress(BaseModel):
    """This object represents a shipping address.

    See here: https://core.telegram.org/bots/api#shippingaddress
    """

    country_code: str = Field(
        description="Two-letter ISO 3166-1 alpha-2 country code",
    )
    state: str = Field(
        description="State, if applicable",
    )
    city: str = Field(
        description="City",
    )
    street_line1: str = Field(
        description="First line for the address",
    )
    street_line2: str = Field(
        description="Second line for the address",
    )
    post_code: str = Field(
        description="Address post code",
    )


class OrderInfo(BaseModel):
    """This object represents information about an order.

    See here: https://core.telegram.org/bots/api#orderinfo
    """

    name: str | None = Field(
        default=None,
        description="User name",
    )
    phone_number: str | None = Field(
        default=None,
        description="User's phone number",
    )
    email: str | None = Field(
        default=None,
        description="User email",
    )
    shipping_address: ShippingAddress | None = Field(
        default=None,
        description="User shipping address",
    )


class SuccessfulPayment(BaseModel):
    """This object contains basic information about a successful payment.

    See here: https://core.telegram.org/bots/api#successfulpayment
    """

    currency: str = Field(
        description="Three-letter ISO 4217 currency code",
    )
    total_amount: int = Field(
        description="Total price in the smallest units of the currency (integer, not float/double)",
    )
    invoice_payload: str = Field(
        description="Bot specified invoice payload",
    )
    shipping_option_id: str | None = Field(
        default=None,
        description="Identifier of the shipping option chosen by the user",
    )
    order_info: OrderInfo | None = Field(
        default=None,
        description="Order information provided by the user",
    )
    telegram_payment_charge_id: str | None = Field(
        default=None,
        description="Telegram payment identifier",
    )
    provider_payment_charge_id: str | None = Field(
        default=None,
        description="Provider payment identifier",
    )


class MessageEntity(BaseModel):
    """This model represents one special entity in a text message.

    For example, hashtags, usernames, URLs, etc.

    See here: https://core.telegram.org/bots/api#messageentity
    """

    type: str = Field( # noqa A003
        description="Type of the entity",
    )
    offset: int = Field(
        description="Offset in UTF-16 code units to the start of the entity",
    )
    length: int = Field(
        description="Length of the entity in UTF-16 code units",
    )
    url: str | None = Field(
        default=None,
        description="For “text_link” only, URL that will be opened after user taps on the text",
    )
    user: User | None = Field(
        default=None,
        description="For “text_mention” only, the mentioned user",
    )
    language: str | None = Field(
        default=None,
        description="For “pre” only, the programming language of the entity text",
    )
    custom_emoji_id: str | None = Field(
        default=None,
        description="For “custom_emoji” only, unique identifier of the custom emoji",
    )


class Message(BaseModel):
    """This model represents a message.

    See here: https://core.telegram.org/bots/api#message
    """

    message_id: int = Field(
        description="",
    )
    message_thread_id: int | None = Field(
        default=None,
        description="",
    )
    from_: User | None = Field(
        default=None,
        alias='from',
    )
    sender_chat: Chat | None = Field(
        default=None,
        description="",
    )
    date: int = Field(
        description="",
    )
    chat: Chat = Field(
        description="",
    )
    forward_from: User | None = Field(
        default=None,
        description="",
    )
    forward_from_chat: Chat | None = Field(
        default=None,
        description="",
    )
    forward_from_message_id: int | None = Field(
        default=None,
        description="",
    )
    forward_signature: str | None = Field(
        default=None,
        description="",
    )
    forward_sender_name: str | None = Field(
        default=None,
        description="",
    )
    forward_date: int | None = Field(
        default=None,
        description="",
    )
    is_topic_message: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    is_automatic_forward: bool | None = Field(
        default=None,
        description="",
    )
    reply_to_message: Optional['Message'] = Field(
        default=None,
        description="",
    )
    via_bot: User | None = Field(
        default=None,
        description="",
    )
    edit_date: int | None = Field(
        default=None,
        description="",
    )
    has_protected_content: bool | None = Field(
        default=None,
        description="",
    )
    media_group_id: str | None = Field(
        default=None,
        description="",
    )
    author_signature: str | None = Field(
        default=None,
        description="",
    )
    text: str | None = Field(
        default=None,
        description="",
    )
    entities: list[MessageEntity] | None = Field(
        default=None,
        description="",
    )
    animation: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    audio: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    document: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    photo: list[dict[str, Any]] | None = Field(
        default=None,
        description="",
    )
    sticker: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    video: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    video_note: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    voice: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    caption: str | None = Field(
        default=None,
        description="",
    )
    caption_entities: list[MessageEntity] | None = Field(
        default=None,
        description="",
    )
    has_media_spoiler: bool | None = Field(
        default=None,
        description="",
    )
    contact: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    dice: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    game: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    poll: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    venue: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    location: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    new_chat_members: list[User] | None = Field(
        default=None,
        description="",
    )
    left_chat_member: User | None = Field(
        default=None,
        description="",
    )
    new_chat_title: str | None = Field(
        default=None,
        description="",
    )
    new_chat_photo: list[dict[str, Any]] | None = Field(
        default=None,
        description="",
    )
    delete_chat_photo: bool | None = Field(
        default=None,
        description="",
    )
    group_chat_created: bool | None = Field(
        default=None,
        description="",
    )
    supergroup_chat_created: bool | None = Field(
        default=None,
        description="",
    )
    channel_chat_created: bool | None = Field(
        default=None,
        description="",
    )
    message_auto_delete_timer_changed: list[dict[str, Any]] | None = Field(
        default=None,
        description="",
    )
    migrate_to_chat_id: int | None = Field(
        default=None,
        description="",
    )
    migrate_from_chat_id: int | None = Field(
        default=None,
        description="",
    )
    pinned_message: Optional['Message'] | None = Field(
        default=None,
        description="",
    )
    invoice: Invoice | None = Field(
        default=None,
        description="",
    )
    successful_payment: SuccessfulPayment | None = Field(
        default=None,
        description="",
    )
    user_shared: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    chat_shared: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    connected_website: str | None = Field(
        default=None,
        description="",
    )
    write_access_allowed: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    passport_data: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    proximity_alert_triggered: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    forum_topic_created: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    forum_topic_edited: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    forum_topic_closed: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    forum_topic_reopened: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    general_forum_topic_hidden: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    general_forum_topic_unhidden: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    video_chat_scheduled: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    video_chat_started: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    video_chat_ended: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    video_chat_participants_invited: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    web_app_data: dict[str, Any] | None = Field(
        default=None,
        description="",
    )
    reply_markup: InlineKeyboardMarkup | None = Field(
        default=None,
        description="",
    )


class MessageReplyMarkup(BaseModel):
    message_reply_markup: Union[Message, bool] = Field(
        description="",
    )


class InputMediaUrlPhoto(BaseModel):
    """This model represents a photo with url or file id.

    See here: https://core.telegram.org/bots/api#inputmediaphoto
    """

    type: str = Field( # noqa A003
        default='photo',
        description="",
    )
    media: str = Field(
        description="",
    )
    caption: str = Field(
        default=None,
        max_length=1024,
        description="",
    )
    parse_mode: str | None = Field(
        default=None,
        description="",
    )
    caption_entities: list[MessageEntity] | None = Field(
        default=None,
        description="",
    )
    has_spoiler: bool | None = Field(
        default=None,
        description="",
    )


class InputMediaBytesPhoto(BaseModel):
    """This model represents a photo with file.

    See here: https://core.telegram.org/bots/api#inputmediaphoto
    """

    type: str = Field( # noqa A003
        default='photo',
        description="",
    )
    media: str = Field(
        description="",
    )
    media_content: bytes = Field(
        description="",
    )
    caption: str = Field(
        default=None,
        max_length=1024,
        description="",
    )
    parse_mode: str | None = Field(
        default=None,
        description="",
    )
    caption_entities: list[MessageEntity] | None = Field(
        default=None,
        description="",
    )
    has_spoiler: bool | None = Field(
        default=None,
        description="",
    )


class InputMediaUrlDocument(BaseModel):
    """This model represents a document with url or file id.

    See here: https://core.telegram.org/bots/api#inputmediadocument
    """

    type: str = Field( # noqa A003
        default='document',
        description="",
    )
    media: str = Field(
        description="",
    )
    thumbnail: str | None = Field(
        default=None,
        description="",
    )
    thumbnail_content: bytes | None = Field(
        default=None,
        description="",
    )
    caption: str = Field(None, max_length=1024)
    parse_mode: str | None = Field(
        default=None,
        description="",
    )
    caption_entities: list[MessageEntity] | None = Field(
        default=None,
        description="",
    )
    disable_content_type_detection: bool | None = Field(
        default=None,
        description="",
    )


class InputMediaBytesDocument(BaseModel):
    """This model represents a document with file.

    See here: https://core.telegram.org/bots/api#inputmediadocument
    """

    type: str = Field( # noqa A003
        default='document',
        description="",
    )
    media: str = Field(
        description="",
    )
    media_content: bytes = Field(
        description="",
    )
    thumbnail: str | None = Field(
        default=None,
        description="",
    )
    thumbnail_content: bytes | None = Field(
        default=None,
        description="",
    )
    caption: str = Field(
        default=None,
        max_length=1024,
        description="",
    )
    parse_mode: str | None = Field(
        default=None,
        description="",
    )
    caption_entities: list[MessageEntity] | None = Field(
        default=None,
        description="",
    )
    disable_content_type_detection: bool | None = Field(
        default=None,
        description="",
    )


class CallbackQuery(BaseModel):
    data: str
    message: Message | None = Field(
        default=None,
        description='New incoming message of any kind - text, photo, sticker, etc.',
    )
    from_: User | None = Field(
        default=None,
        alias='from',
        description="",
    )
    chat_instance: str | None = Field(
        default=None,
        description="",
    )


class Location(BaseModel):
    """This object represents a point on the map.

    See here: https://core.telegram.org/bots/api#location
    """

    longitude: float = Field(
        description="",
    )
    latitude: float = Field(
        description="",
    )
    horizontal_accuracy: float | None = Field(
        default=None,
        description="",
    )
    live_period: int | None = Field(
        default=None,
        description="",
    )
    heading: int | None = Field(
        default=None,
        description="",
    )
    proximity_alert_radius: int | None = Field(
        default=None,
        description="",
    )


class InlineQuery(BaseModel):
    """This object represents an incoming inline query.

    When the user sends an empty query, your bot could return some default or trending results.
    See here: https://core.telegram.org/bots/api#inlinequery
    """

    id: str = Field( # noqa A003
        description="",
    )
    from_: User = Field(
        alias='from',
        description="",
    )
    query: str = Field(
        description="",
    )
    offset: str = Field(
        description="",
    )
    chat_type: str | None = Field(
        default=None,
        description="",
    )
    location: Location | None = Field(
        default=None,
        description="",
    )


class ChosenInlineResult(BaseModel):
    """Represents a result of an inline query that was chosen by the user and sent to their chat partner.

    Note: It is necessary to enable inline feedback via @BotFather in order to receive these objects in updates.
    See here: https://core.telegram.org/bots/api#choseninlineresult
    """

    result_id: str = Field(
        description="",
    )
    from_: User = Field(
        alias='from',
        description="",
    )
    location: Location | None = Field(
        default=None,
        description="",
    )
    inline_message_id: str | None = Field(
        default=None,
        description="",
    )
    query: str | None = Field(
        default=None,
        description="",
    )


class ShippingQuery(BaseModel):
    """This object contains information about an incoming shipping query.

    See here: https://core.telegram.org/bots/api#shippingquery
    """

    id: str = Field( # noqa A003
        description="",
    )
    from_: User = Field(
        alias='from',
        description="",
    )
    invoice_payload: str = Field( # noqa A003
        description="",
    )
    shipping_address: ShippingAddress = Field(
        description="",
    )


class PreCheckoutQuery(BaseModel):
    """This object contains information about an incoming pre-checkout query.

    See here: https://core.telegram.org/bots/api#shippingquery
    """

    id: str = Field( # noqa A003
        description="",
    )
    from_: User = Field(
        alias='from',
        description="",
    )
    currency: str = Field(
        description="",
    )
    total_amount: int
    invoice_payload: str = Field(
        description="",
    )
    shipping_option_id: str | None = Field(
        default=None,
        description="",
    )
    order_info: OrderInfo | None = Field(
        default=None,
        description="",
    )


class PollOption(BaseModel):
    """This object contains information about one answer option in a poll.

    See here: https://core.telegram.org/bots/api#polloption
    """

    text: str = Field(
        description="",
    )
    voter_count: int = Field(
        description="",
    )


class Poll(BaseModel):
    """This object contains information about a poll.

    See here: https://core.telegram.org/bots/api#poll
    """

    id: str = Field( # noqa A003
        description="",
    )
    question: str = Field(
        description="",
    )
    options: list[PollOption] = Field(
        description="",
    )
    total_voter_count: int = Field(
        description="",
    )
    is_closed: bool = Field(
        description="",
    )
    is_anonymous: bool = Field( # noqa A003
        description="",
    )
    type: str = Field( # noqa A003
        description="",
    )
    allows_multiple_answers: bool
    correct_option_id: int | None = Field( # noqa A003
        default=None,
        description="",
    )
    explanation: str | None = Field(
        default=None,
        description="",
    )
    explanation_entities: list[MessageEntity] | None = Field(
        default=None,
        description="",
    )
    open_period: int | None = Field(
        default=None,
        description="",
    )
    close_date: int | None = Field(
        default=None,
        description="",
    )


class PollAnswer(BaseModel):
    """This object represents an answer of a user in a non-anonymous poll.

    See here: https://core.telegram.org/bots/api#pollanswer
    """

    poll_id: str = Field(
        description="",
    )
    user: User = Field(
        description="",
    )
    option_ids: list[int] = Field(
        description="",
    )


class ChatInviteLink(BaseModel):
    """Represents an invite link for a chat.

    See here: https://core.telegram.org/bots/api#chatinvitelink
    """

    invite_link: str = Field(
        description="",
    )
    creator: User = Field(
        description="",
    )
    creates_join_request: bool = Field(
        description="",
    )
    is_primary: bool = Field(
        description="",
    )
    is_revoked: bool = Field(
        description="",
    )
    name: str | None = Field(
        default=None,
        description="",
    )
    expire_date: int | None = Field(
        default=None,
        description="",
    )
    member_limit: int | None = Field(
        default=None,
        description="",
    )
    pending_join_request_count: int | None = Field(
        default=None,
        description="",
    )


class ChatJoinRequest(BaseModel):
    """Represents a join request sent to a chat.

    See here: https://core.telegram.org/bots/api#chatjoinrequest
    """

    chat: Chat = Field(
        description="",
    )
    from_: User = Field(
        alias='from',
        description="",
    )
    user_chat_id: int = Field(
        description="",
    )
    date: int = Field(
        description="",
    )
    bio: str | None = Field(
        default=None,
        description="",
    )
    invite_link: ChatInviteLink | None = Field(
        default=None,
        description="",
    )


class ChatMemberOwner(BaseModel):
    """Represents a join request sent to a chat.

    See here: https://core.telegram.org/bots/api#chatmemberowner
    """

    status: str = Field(
        description="",
    )
    user: User = Field(
        description="",
    )
    is_anonymous: bool = Field(
        description="",
    )
    custom_title: str = Field(
        description="",
    )


class ChatMemberAdministrator(BaseModel):
    """Represents a join request sent to a chat.

    See here: https://core.telegram.org/bots/api#chatmemberadministrator
    """

    status: str = Field(
        description="",
    )
    user: User = Field(
        description="",
    )
    can_be_edited: bool = Field(
        description="",
    )
    is_anonymous: bool = Field(
        description="",
    )
    can_manage_chat: bool = Field(
        description="",
    )
    can_delete_messages: bool = Field(
        description="",
    )
    can_manage_video_chats: bool = Field(
        description="",
    )
    can_restrict_members: bool = Field(
        description="",
    )
    can_promote_members: bool = Field(
        description="",
    )
    can_change_info: bool = Field(
        description="",
    )
    can_invite_users: bool = Field(
        description="",
    )
    can_post_messages: bool = Field(
        description="",
    )
    can_edit_messages: bool = Field(
        description="",
    )
    can_pin_messages: bool = Field(
        description="",
    )
    can_manage_topics: bool = Field(
        description="",
    )
    custom_title: bool = Field(
        description="",
    )


class ChatMemberMember(BaseModel):
    """Represents a join request sent to a chat.

    See here: https://core.telegram.org/bots/api#chatmembermember
    """

    status: str = Field(
        description="",
    )
    user: User = Field(
        description="",
    )


class ChatMemberRestricted(BaseModel):
    """Represents a join request sent to a chat.

    See here: https://core.telegram.org/bots/api#chatmemberrestricted
    """

    status: str = Field(
        description="",
    )
    user: User = Field(
        description="",
    )
    is_member: bool = Field(
        description="",
    )
    can_send_messages: bool = Field(
        description="",
    )
    can_send_audios: bool = Field(
        description="",
    )
    can_send_documents: bool = Field(
        description="",
    )
    can_send_photos: bool = Field(
        description="",
    )
    can_send_videos: bool = Field(
        description="",
    )
    can_send_video_notes: bool = Field(
        description="",
    )
    can_send_voice_notes: bool = Field(
        description="",
    )
    can_send_polls: bool = Field(
        description="",
    )
    can_send_other_messages: bool = Field(
        description="",
    )
    can_add_web_page_previews: bool = Field(
        description="",
    )
    can_change_info: bool = Field(
        description="",
    )
    can_invite_users: bool = Field(
        description="",
    )
    can_pin_messages: bool = Field(
        description="",
    )
    can_manage_topics: bool = Field(
        description="",
    )
    until_date: bool = Field(
        description="",
    )


class ChatMemberLeft(BaseModel):
    """Represents a join request sent to a chat.

    See here: https://core.telegram.org/bots/api#chatmemberleft
    """

    status: str = Field(
        description="",
    )
    user: User = Field(
        description="",
    )


class ChatMemberBanned(BaseModel):
    """Represents a join request sent to a chat.

    See here: https://core.telegram.org/bots/api#chatmemberbanned
    """

    status: str = Field(
        description="",
    )
    user: User = Field(
        description="",
    )
    until_date: int = Field(
        description="",
    )


class ChatMemberUpdated(BaseModel):
    """This object represents changes in the status of a chat member.

    See here: https://core.telegram.org/bots/api#chatmemberupdated
    """

    chat: Chat = Field(
        description="",
    )
    from_: User = Field(
        description="",
    )
    date: int = Field(
        description="",
    )
    old_chat_member: Union[
        ChatMemberOwner,
        ChatMemberAdministrator,
        ChatMemberMember,
        ChatMemberRestricted,
        ChatMemberLeft,
        ChatMemberBanned,
    ] = Field(
        description="",
    )
    new_chat_member: Union[
        ChatMemberOwner,
        ChatMemberAdministrator,
        ChatMemberMember,
        ChatMemberRestricted,
        ChatMemberLeft,
        ChatMemberBanned,
    ] = Field(
        description="",
    )
    invite_link: ChatInviteLink | None = Field(
        default=None,
        description="",
    )
    via_chat_folder_invite_link: bool = Field(
        description="",
    )


class Update(BaseModel):
    """This object represents an incoming update.

    See here: https://core.telegram.org/bots/api#update
    """

    update_id: int = Field(
        description="",
    )
    message: Message | None = Field(
        default=None,
        description='New incoming message of any kind - text, photo, sticker, etc.',
    )
    edited_message: Message | None = Field(
        description='New version of a message that is known to the bot and was edited',
    )
    channel_post: Message | None = Field(
        description='New incoming channel post of any kind - text, photo, sticker, etc.',
    )
    edited_channel_post: Message | None = Field(
        description='New version of a channel post that is known to the bot and was edited',
    )
    inline_query: InlineQuery | None = Field(
        default=None,
        description="",
    )
    chosen_inline_result: ChosenInlineResult | None = Field(
        default=None,
        description="",
    )
    callback_query: CallbackQuery | None = Field(
        default=None,
        description="",
    )
    shipping_query: ShippingQuery | None = Field(
        default=None,
        description="",
    )
    pre_checkout_query: PreCheckoutQuery | None = Field(
        default=None,
        description="",
    )
    poll: Poll | None = Field(
        default=None,
        description="",
    )
    poll_answer: PollAnswer | None = Field(
        default=None,
        description="",
    )
    my_chat_member: ChatMemberUpdated | None = Field(
        default=None,
        description="",
    )
    chat_member: ChatMemberUpdated | None = Field(
        default=None,
        description="",
    )
    chat_join_request: ChatJoinRequest | None = Field(
        default=None,
        description="",
    )

    # TODO At most one of the optional parameters can be present in any given update.


# fix ForwardRef fpr cyclic refernces Chat --> Message --> Chat
Chat.update_forward_refs()
