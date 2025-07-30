from .api_command import command_action
from .api_group import info_action
from .api_message import message_action
from .bot import ChatBot

command_action(ChatBot)
info_action(ChatBot)
message_action(ChatBot)

__all__ = ["ChatBot"]
