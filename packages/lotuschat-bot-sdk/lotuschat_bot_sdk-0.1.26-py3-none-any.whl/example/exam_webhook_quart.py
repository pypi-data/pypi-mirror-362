from quart import Quart

from exam_other_const import TOKEN_STICKER_DOWNLOAD_BOT
from src.example.exam_other_const import CHAT_ID_SINGLE, PORT
from src.lotuschat_sdk.control import ChatBot
from src.lotuschat_sdk.control.bot import Argument, ErrorType
from src.lotuschat_sdk.model.message import Message, Updates
from src.lotuschat_sdk.model.notify import NotifyEvent, NewChatMemberPayload, BaseNotifyPayload, LeftChatMemberPayload
from src.lotuschat_sdk.utility.logger import log_verbose, log_debug, log_info, log_warning


# Class testing
class Test:
    def __init__(self):
        self._name = "Test Quart"

    bot = ChatBot(
        name="sticker_download_bot",
        token=TOKEN_STICKER_DOWNLOAD_BOT,
        is_log_curl_command=True
    )

    async def on_errors(self, error_type: ErrorType, error: str):
        log_warning(f"{self._name} receive error[{error_type}] from bot: {error}")

    async def on_self_messages(self, text: str, chat_id: int, message: Message, updates: Updates):
        log_verbose(f"{self._name} receive this bot {chat_id} message {text}")

    async def on_messages(self, text: str, chat_id: int, message: Message, updates: Updates):
        log_verbose(f"{self._name} receive all message with message[{text}] from {chat_id}")
        if message.entities:
            result = self.bot.entity_extract(text, message.entities)
            log_debug(result)

    async def on_messages_no_command(self, text: str, chat_id: int, message: Message, updates: Updates):
        log_verbose(f"{self._name} receive all message with no command with message[{text}] from {chat_id}")

    async def on_commands(self, command: str, args: list[Argument], chat_id: int, message: Message, updates: Updates):
        log_verbose(f"{self._name} receive all command with command {command} from {chat_id} has arguments {args}")

    async def on_temp_command(self, args: list[Argument], chat_id: int, message: Message, updates: Updates):
        log_verbose(f"{self._name} handle temp command with arguments {args} from {chat_id}")
        await self.bot.get_messages(
            offset=0, limit=10
        )
        await self.bot.send_message(
            chat_id=CHAT_ID_SINGLE,
            text=f"python bot receive temp command from quart setup with arguments[{args}]"
        )

    async def on_notify(self, notify_type: NotifyEvent, params: BaseNotifyPayload, message: Message, updates: Updates):
        if notify_type == NotifyEvent.NEW_CHAT_MEMBERS:
            if isinstance(params, NewChatMemberPayload):
                log_info(f"{self._name} on_notify event NEW_CHAT_MEMBERS with payload {params.payload}")
        elif notify_type == NotifyEvent.LEFT_CHAT_MEMBERS:
            if isinstance(params, LeftChatMemberPayload):
                log_info(f"{self._name} on_notify event LEFT_CHAT_MEMBERS with payload {params.payload}")

    def run(self):
        log_info(f"create bot[{self}] to test send message")
        log_debug(self.bot)

        log_info("setting listener & receive message event")
        self.bot.set_on_errors(self.on_errors)
        self.bot.set_self_messages(self.on_self_messages)
        self.bot.set_on_messages(self.on_messages)
        self.bot.set_on_notify(self.on_notify)
        self.bot.set_on_messages(self.on_messages_no_command, is_get_command=False)
        self.bot.set_on_commands(self.on_commands)
        self.bot.set_on_command("/temp", self.on_temp_command)


# Running
control = Test()

app = Quart(__name__)


@app.route("/", methods=["POST"])
async def lc_webhook():
    result = await control.bot.web_hook_quart()
    log_verbose(result)
    return result


if __name__ == "__main__":
    control.run()
    app.run(port=PORT)
