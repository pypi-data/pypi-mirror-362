import json
from dataclasses import asdict

import aiohttp

from ..model.request import RestrictChatPermission, PromotePermission, ChatPermission


def info_action(cls):
    async def get_chat(self, chat_id: int):
        url = f"{self._domain}{self._token}/getChat"
        payload = aiohttp.FormData()
        payload.add_field("chat_id", chat_id)
        return await self._request(url, payload)

    async def get_chat_administrators(self, chat_id: int):
        url = f"{self._domain}{self._token}/getChatAdministrators"
        payload = aiohttp.FormData()
        payload.add_field("chat_id", chat_id)
        return await self._request(url, payload)

    async def get_chat_member(self, chat_id: int, user_id: int):
        url = f"{self._domain}{self._token}/getChatMember"
        payload = aiohttp.FormData()
        payload.add_field("chat_id", chat_id)
        payload.add_field("user_id", user_id)
        return await self._request(url, payload)

    async def get_chat_member_count(self, chat_id: int):
        url = f"{self._domain}{self._token}/getChatMemberCount"
        payload = aiohttp.FormData()
        payload.add_field("chat_id", chat_id)
        return await self._request(url, payload)

    async def leave_chat(self, chat_id: int):
        url = f"{self._domain}{self._token}/leaveChat"
        payload = aiohttp.FormData()
        payload.add_field("chat_id", chat_id)
        return await self._request(url, payload)

    async def ban_chat_member(self, chat_id: int, user_id: int):
        url = f"{self._domain}{self._token}/banChatMember"
        payload = aiohttp.FormData()
        payload.add_field("chat_id", chat_id)
        payload.add_field("user_id", user_id)
        return await self._request(url, payload)

    async def un_ban_chat_member(self, chat_id: int, user_id: int):
        url = f"{self._domain}{self._token}/unBanChatMember"
        payload = aiohttp.FormData()
        payload.add_field("chat_id", chat_id)
        payload.add_field("user_id", user_id)
        return await self._request(url, payload)

    async def restrict_chat_member(self, chat_id: int, user_id: int, until_date: int,
                                   permissions: RestrictChatPermission):
        url = f"{self._domain}{self._token}/retrictChatMember"
        payload = aiohttp.FormData()
        payload.add_field("chat_id", chat_id)
        payload.add_field("user_id", user_id)
        payload.add_field("until_date", until_date)
        payload.add_field("permissions", permissions.model_dump_json())
        return await self._request(url, payload)

    async def promote_chat_member(self, chat_id: int, user_id: int, is_anonymous: bool,
                                  disable_admin_setting_notify: bool,
                                  promote_permission: PromotePermission):
        url = f"{self._domain}{self._token}/promoteChatMember"
        payload = aiohttp.FormData()
        payload.add_field("chat_id", chat_id)
        payload.add_field("user_id", user_id)
        payload.add_field("is_anonymous", is_anonymous)
        payload.add_field("disable_admin_setting_notify", disable_admin_setting_notify)
        for key, value in promote_permission.to_dict().items():
            payload.add_field(key, str(value))
        return await self._request(url, payload)

    async def approve_chat_join_request(self, chat_id: int, user_id: int):
        url = f"{self._domain}{self._token}/approveChatJoinRequest"
        payload = aiohttp.FormData()
        payload.add_field("chat_id", chat_id)
        payload.add_field("user_id", user_id)
        return await self._request(url, payload)

    async def decline_chat_join_request(self, chat_id: int, user_id: int):
        url = f"{self._domain}{self._token}/declineChatJoinRequest"
        payload = aiohttp.FormData()
        payload.add_field("chat_id", chat_id)
        payload.add_field("user_id", user_id)
        return await self._request(url, payload)

    async def set_chat_permission(self, chat_id: int, permissions: ChatPermission):
        url = f"{self._domain}{self._token}/setChatPermissions"
        payload = aiohttp.FormData()
        payload.add_field("chat_id", chat_id)
        payload.add_field("permissions", permissions.model_dump_json())
        return await self._request(url, payload)

    # Attach async methods to the class
    cls.get_chat = get_chat
    cls.get_chat_administrators = get_chat_administrators
    cls.get_chat_member = get_chat_member
    cls.get_chat_member_count = get_chat_member_count
    cls.leave_chat = leave_chat
    cls.ban_chat_member = ban_chat_member
    cls.un_ban_chat_member = un_ban_chat_member
    cls.restrict_chat_member = restrict_chat_member
    cls.promote_chat_member = promote_chat_member
    cls.approve_chat_join_request = approve_chat_join_request
    cls.decline_chat_join_request = decline_chat_join_request
    cls.set_chat_permission = set_chat_permission
    return cls
