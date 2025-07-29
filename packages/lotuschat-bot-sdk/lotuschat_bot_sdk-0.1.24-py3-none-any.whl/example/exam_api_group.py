import asyncio

from exam_other_const import TOKEN_STICKER_DOWNLOAD_BOT, CHAT_ID_GROUP
from src.example.exam_other_const import CHAT_ID_SINGLE, BAN_ID
from src.lotuschat_sdk.control.bot import ChatBot
from src.lotuschat_sdk.model.request import RestrictChatPermission, PromotePermission, ChatPermission
from src.lotuschat_sdk.utility.logger import log_verbose

bot = ChatBot(
    name="Python Bot - Test command event",
    token=TOKEN_STICKER_DOWNLOAD_BOT,
    is_vpn=True
)


async def command():
    get_chat = bot.get_chat(chat_id=CHAT_ID_GROUP)
    get_administrators = bot.get_chat_administrators(chat_id=CHAT_ID_GROUP)
    get_member = bot.get_chat_member(chat_id=CHAT_ID_GROUP, user_id=CHAT_ID_SINGLE)
    get_member_count = bot.get_chat_member_count(chat_id=CHAT_ID_GROUP)
    ban_chat_member = bot.ban_chat_member(chat_id=CHAT_ID_GROUP, user_id=BAN_ID)
    un_ban_chat_member = bot.un_ban_chat_member(chat_id=CHAT_ID_GROUP, user_id=BAN_ID)
    restrict_chat_member = bot.restrict_chat_member(chat_id=CHAT_ID_GROUP, user_id=BAN_ID, until_date=1752048738,
                                                    permissions=RestrictChatPermission(send_messages=True, send_photos=True))
    promote_chat_member = bot.promote_chat_member(chat_id=CHAT_ID_GROUP, user_id=BAN_ID,
                                                  promote_permission=PromotePermission(can_change_info=True),
                                                  is_anonymous=True, disable_admin_setting_notify=True)
    approve_chat_join_request = bot.approve_chat_join_request(chat_id=CHAT_ID_GROUP, user_id=BAN_ID)
    decline_chat_join_request = bot.decline_chat_join_request(chat_id=CHAT_ID_GROUP, user_id=BAN_ID)
    set_chat_permission = bot.set_chat_permission(chat_id=CHAT_ID_GROUP,
                                                  permissions=ChatPermission(until_date=1720000000, send_media=True))

    results = await asyncio.gather(
        get_chat,
        get_administrators,
        get_member,
        get_member_count,
        ban_chat_member,
        un_ban_chat_member,
        restrict_chat_member,
        promote_chat_member,
        approve_chat_join_request,
        decline_chat_join_request,
        set_chat_permission,
        return_exceptions=True
    )
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            log_verbose(f"Task {i + 1} failed: {result}")
        else:
            log_verbose(f"Task {i + 1} success: {result}")


asyncio.run(command())
