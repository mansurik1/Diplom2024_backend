import json
import asyncio
from asyncio import Task
from typing import Optional

from app.store import Store
from logging import getLogger
from app.store.broker.producer import new_task


class Poller:
    def __init__(self, store: Store):
        self.store = store
        self.logger = getLogger("poller")
        self.is_running = False
        self.poll_task: Optional[Task] = None

    async def start(self):
        self.logger.info("start polling")
        self.is_running = True
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self):
        self.logger.info("stop polling")
        self.is_running = False
        self.poll_task.cancel()

    async def poll(self):
        offset = 0
        while self.is_running:
            updates = await self.store.tg_api.get_updates(offset=offset, timeout=60)
            for upd in updates["result"]:
                new_task(upd)
                offset = upd["update_id"] + 1
