import os
import json
import typing
from logging import getLogger

from app.store.bot.utils.is_auth import is_auth
from app.store.bot.utils.lab_rep_proc import lab_rep_proc
from app.store.bot.utils.redis_ import redis_save_data, redis_get_data
from app.store.bot.utils.week_fraction import week_fraction
from app.store.bot.utils.msgs import (
    COMMANDS,
    START,
    HELP,
    TODAY
)
from app.store.tg_api.dataclasses import UpdateObj

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BotWorker:
    def __init__(self, app: "Application"):
        self.app = app
        self.logger = getLogger("handler")

    async def handle_update(self, body: dict):
        upd: UpdateObj = UpdateObj.Schema().load(body)

        try:
            match upd.message.text:
                case "/start":
                    await self.app.store.tg_api.send_message(
                        upd.message.chat.id,
                        START
                    )

                case "/help":
                    await self.app.store.tg_api.send_message(
                        upd.message.chat.id,
                        HELP
                    )

                case "/week":
                    await self.app.store.tg_api.send_message(
                        upd.message.chat.id,
                        TODAY + week_fraction()
                    )

                case "/calendar":
                    await self.app.store.tg_api.send_calendar(
                        upd.message.chat.id
                    )

                case "/login":
                    redirect_uri = "http://127.0.0.1:8000/oauth_callback"
                    auth_url = f"https://science.iu5.bmstu.ru/sso/authorize?redirect_uri={redirect_uri}"
                    reply = {
                        "keyboard": [
                            [{"text": "Авторизироваться", "web_app": {"url": auth_url}}]
                        ],
                        "resize_keyboard": True,
                        "selective": True
                    }
                    await self.app.store.tg_api.authorize(
                        upd.message.chat.id,
                        "Ниже появится кнопка",
                        json.dumps(reply)
                    )


                case _:
                    await self.app.store.tg_api.send_message(
                        upd.message.chat.id,
                        f"Такой команды нет. {COMMANDS}",
                    )

        except Exception as err:
            self.logger.info(f"Error while handling upd: {err}")
            await self.app.store.tg_api.send_message(
                upd.message.chat.id,
                f"Такой команды нет. {COMMANDS}",
            )

    async def handle_text(self, body: dict):
        upd: UpdateObj = UpdateObj.Schema().load(body)

        cmd = redis_get_data(f"{upd.message.chat.id}:cmd")
        match cmd:
            case "lab_rep":
                match lab_rep_proc(upd.message.chat.id, upd.message.text):
                    case 1:
                        await self.app.store.tg_api.send_message(
                            upd.message.chat.id,
                            "ЛР/ДЗ"
                        )

                    case 2:
                        await self.app.store.tg_api.send_message(
                            upd.message.chat.id,
                            "Номер ЛР/ДЗ"
                        )

                    case 3:
                        await self.app.store.tg_api.send_message(
                            upd.message.chat.id,
                            "Кидай отчет"
                        )

            case _:
                await self.app.store.tg_api.send_message(
                    upd.message.chat.id,
                    "Выбери команду"
                )

    async def handle_docs(self, body: dict):
        upd: UpdateObj = UpdateObj.Schema().load(body)

        file_id = upd.message.document.file_id
        file_name = lab_rep_proc(upd.message.chat.id)
        dir_path = os.path.join(
            os.path.dirname(os.path.realpath("chat_bot")), "lab_reports"
        )

        doc = await self.app.store.tg_api.get_document(file_id)
        doc_path = doc.result.file_path

        await self.app.store.tg_api.download_document(
            doc_path, file_name, dir_path
        )

        await self.app.store.tg_api.send_message(
            upd.message.chat.id,
            "Отчет успешно отправлен"
        )

    async def handle_web_app(self, body: dict):
        upd: UpdateObj = UpdateObj.Schema().load(body)

        redis_save_data(f"{upd.message.chat.id}:info", upd.message.web_app_data.data)
