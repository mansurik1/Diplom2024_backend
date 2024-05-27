import typing
from typing import Optional
from aiohttp import ClientSession, TCPConnector
from app.base.base_accessor import BaseAccessor
from app.store.tg_api.dataclasses import (
    GetUpdatesResponse,
    SendMessageResponse,
    SendMessageErrorResponse,
    GetDocumentResponse
)
from app.store.tg_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application

API_URL = "https://api.telegram.org/bot"


class TgApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: Optional[ClientSession] = None
        self.token = app.config.bot.token

    async def connect(self, app: "Application"):
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))
        self.poller = Poller(app.store)
        await self.poller.start()

    async def disconnect(self, app: "Application"):
        if self.session:
            await self.session.close()
        if self.poller:
            await self.poller.stop()

    def get_url(self, method: str):
        return f"{API_URL}{self.token}/{method}"
    
    async def get_me(self) -> dict:
        url = self.get_url("getMe")
        async with self.session.get(
            url=url
        ) as resp:
            return await resp.json()

    async def get_updates(
        self,
        offset: Optional[int] = None,
        timeout: int = 0
    ) -> dict:
        url = self.get_url("getUpdates")
        params = {}
        if offset:
            params["offset"] = offset
        if timeout:
            params["timeout"] = timeout
        async with self.session.get(
            url=url,
            params=params
        ) as resp:
            return await resp.json()

    async def get_updates_in_objects(
        self,
        offset: Optional[int] = None,
        timeout: int = 0
    ) -> GetUpdatesResponse:
        """
        Преобразует ответ json формата в объекты python
        для удобной работы с ними.
        """
        res_dict = await self.get_updates(offset=offset, timeout=timeout)
        self.logger.info(res_dict)
        return GetUpdatesResponse.Schema().load(res_dict)

    async def send_calendar(
        self,
        chat_id: int
    ):
        url = self.get_url("sendMessage")
        params = {
            "chat_id": chat_id,
            "text": "Календарь"
        }
        body = {
            "reply_markup": {
                "inline_keyboard": [[
                    {"text": "Открыть", "web_app": {"url": "https://mansurik1.github.io/Diplom2024?chat_id=595866181"}}
                ]]}
        }
        async with self.session.get(
                url=url,
                params=params,
                json=body
        ) as resp:
            res_dict = await resp.json()
            return SendMessageResponse.Schema().load(res_dict)
    async def send_message(
        self,
        chat_id: int,
        text: str,
        reply: Optional[str] = None
    ) -> SendMessageResponse | SendMessageErrorResponse:
        url = self.get_url("sendMessage")
        params = {
            "chat_id": chat_id,
            "text": text,
        }
        if reply:
            params["reply_markup"] = reply
        async with self.session.get(
            url=url,
            params=params
        ) as resp:
            res_dict = await resp.json()

            if res_dict["ok"]:
                return SendMessageResponse.Schema().load(res_dict)
            else:
                return SendMessageErrorResponse.Schema().load(res_dict)

    async def authorize(
            self,
            chat_id: int,
            text: [str],
            reply: Optional[str] = None
    ):
        url = self.get_url("sendMessage")
        params = {
            "chat_id": chat_id,
            "text": text
        }
        if reply:
            params["reply_markup"] = reply
        async with self.session.get(
                url=url,
                params=params
        ) as resp:
            res_dict = await resp.json()
            return SendMessageResponse.Schema().load(res_dict)

    async def send_document(
        self,
        chat_id: int,
        file_id: str
    ):
        url = self.get_url("sendDocument")
        params = {
            "chat_id": chat_id,
            "document": file_id
        }
        async with self.session.get(
            url=url,
            params=params
        ) as resp:
            res_dict = await resp.json()
            return SendMessageResponse.Schema().load(res_dict)

    async def get_document(
        self,
        file_id: str,
    ) -> GetDocumentResponse:
        url = self.get_url("getFile")
        params = {
            "file_id": file_id,
        }
        async with self.session.get(
            url=url,
            params=params
        ) as resp:
            res_dict = await resp.json()
            return GetDocumentResponse.Schema().load(res_dict)

    async def download_document(
        self,
        file_path: str,
        file_name: str,
        dir_to_save_path: str
    ) -> None:
        url = f"https://api.telegram.org/file/bot{self.token}/{file_path}"
        dest_path = f"{dir_to_save_path}/{file_name}"
        async with self.session.get(
            url=url
        ) as resp:
            assert resp.status == 200
            with open(dest_path, "wb") as f:
                while True:
                    chunk = await resp.content.readany()
                    if not chunk:
                        break
                    f.write(chunk)

