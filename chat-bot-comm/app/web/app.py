from typing import Optional

from aiohttp.web import (
    Application as AiohttpApplication,
    View as AiohttpView,
    Request as AiohttpRequest,
)
from aiohttp_apispec import setup_aiohttp_apispec

from app.store import Store, setup_store
from app.web.config import Config, setup_config
from app.web.logger import setup_logging
from app.web.middlewares import setup_middlewares
from app.web.routes import setup_routes
from app.store.broker.consumer import setup_rabbitmq, close_rabbitmq

class Application(AiohttpApplication):
    config: Optional[Config] = None
    store: Optional[Store] = None
    database = None


class Request(AiohttpRequest):
    @property
    def app(self) -> Application:
        return super().app()


app = Application()
app.on_startup.append(setup_rabbitmq)
app.on_cleanup.append(close_rabbitmq)


def setup_app(config_path: str) -> Application:
    setup_logging(app)
    setup_config(app, config_path)
    setup_routes(app)
    setup_aiohttp_apispec(
        app, title="Tg Chat Bot", url="/docs/json", swagger_path="/docs"
    )
    setup_middlewares(app)
    setup_store(app)    
    return app
