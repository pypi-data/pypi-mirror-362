from enum import Enum
from typing import List

from pydantic import BaseModel, Field


# ####################################################################################################
# key reply_markup - api send message
# ####################################################################################################
class BaseKeyboard(BaseModel): pass


class KeyboardMarkup(BaseModel):
    text: str
    callback_data: str


class InlineKeyboardMarkup(BaseKeyboard):
    inline_keyboard: List[List[KeyboardMarkup]] = Field(default=None)


class ReplyKeyboardMarkup(BaseKeyboard):
    keyboard: List[List[KeyboardMarkup]] = Field(default=None)
    resize_keyboard: bool = Field(default=None)
    one_time_keyboard: bool = Field(default=None)
    selective: bool = Field(default=None)


class ReplyKeyboardRemove(BaseKeyboard):
    remove_keyboard: bool = Field(default=None)
    selective: bool = Field(default=None)


class ForceReply(BaseKeyboard):
    force_reply: bool = Field(default=None)
    selective: bool = Field(default=None)


# ####################################################################################################
# other
# ####################################################################################################
class ParseModeType(Enum):
    MARKDOWN = "Markdown"
    HTML = "HTML"


class ChatAction(Enum):
    TYPING = "typing"
    UPLOAD_PHOTO = "upload_photo"
    RECORD_VIDEO = "record_video"
    UPLOAD_VIDEO = "upload_video"
    RECORD_VOICE = "record_voice"
    UPLOAD_VOICE = "upload_voice"
    UPLOAD_DOCUMENT = "upload_document"
    CHOOSE_STICKER = "choose_sticker"
    FIND_LOCATION = "find_location"
    RECORD_VIDEO_NOTE = "record_video_note"
    UPLOAD_VIDEO_NOTE = "upload_video_note"


class Command(BaseModel):
    command: str
    description: str


class RestrictChatPermission(BaseModel):
    send_messages: bool = False
    send_media: bool = False
    send_photos: bool = False
    send_videos: bool = False
    send_stickers: bool = False
    send_gifs: bool = False
    send_sticker_voices: bool = False
    send_audios: bool = False
    send_files: bool = False
    send_voices: bool = False
    send_roundvideos: bool = False
    embed_links: bool = False
    send_invite_link: bool = False
    change_info: bool = False
    invite_users: bool = False
    pin_messages: bool = False
    contribute_stickers: bool = False


class PromotePermission(BaseModel):
    can_change_info: bool = False
    can_post_messages: bool = False
    can_ban_members: bool = False
    can_delete_messages: bool = False
    can_invite_members: bool = False
    can_invite_link: bool = False
    can_pin_messages: bool = False
    can_add_admins: bool = False
    can_edit_messages: bool = False
    can_manage_call: bool = False
    can_approve_reaction: bool = False

    def to_dict(self):
        return self.__dict__


class ChatPermission(BaseModel):
    view_messages: bool = False
    send_messages: bool = False
    send_media: bool = False
    send_photos: bool = False
    send_videos: bool = False
    send_stickers: bool = False
    send_gifs: bool = False
    send_audios: bool = False
    send_files: bool = False
    send_voices: bool = False
    send_roundvideos: bool = False
    embed_links: bool = False
    invite_users: bool = False
    send_invite_link: bool = False
    pin_messages: bool = False
    change_info: bool = False
    contribute_stickers: bool = False
    others: bool = False
    send_games: bool = False
    create_convo: bool = False
    send_inline: bool = False
    send_polls: bool = False
    send_sticker_voices: bool = False
    until_date: int
    screen_capture: bool = False

    def to_dict(self):
        return self.__dict__
