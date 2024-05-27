import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Store:
    def __init__(self, app: "Application", *args, **kwargs):
        from app.store.tg_api.api import TgApiAccessor
        from app.store.bot.worker import BotWorker

        self.tg_api = TgApiAccessor(app)
        self.bots_worker = BotWorker(app)

def setup_store(app: "Application"):
    app.store = Store(app)    
