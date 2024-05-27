import json
import asyncio
import aio_pika
import aiormq
from logging import getLogger
from aiohttp import web


logger = getLogger("CONSUMER")


async def setup_rabbitmq(app: web.Application) -> None:
    """
    Open connection to RabbitMQ and create listener task, 
    try to reconnect every 10 seconds if there is a problem.
    """
    # config = app["config"]
    loop = asyncio.get_event_loop()
    try:
        connection: aio_pika.Connection = await aio_pika.connect_robust(host='localhost', loop=loop)
    except (ConnectionError, aiormq.exceptions.IncompatibleProtocolError) as e:
        logger.error(f"action=setup_rabbitmq, status=fail, retry=10s, {e}")
        await asyncio.sleep(10)
        await setup_rabbitmq(app)

        return None

    app["rabbitmq"] = connection
    app["rabbitmq_listener"] = asyncio.create_task(listen_events(app))

    logger.info(f"action=setup_rabbitmq, status=success")


async def close_rabbitmq(app: web.Application) -> None:
    if app.get("rabbitmq_listener"):
        app["rabbitmq_listener"].cancel()
        await app["rabbitmq_listener"]
    if app.get("rabbitmq"):
        await app["rabbitmq"].close()
    logger.info("action=close_rabbitmq, status=success")


async def consume_messages(app: web.Application, queue: aio_pika.Queue) -> None:
    """ Start listening for messages from the specified queue. """
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            logger.info(f" [x] Recieved {message.body}")
            await on_message(app, message)


async def on_message(app, message: aio_pika.IncomingMessage) -> None:
    """ Choose a handler for message processing by routing key. """
    handlers = {
        "cmds": app.store.bots_worker.handle_update,
        "docs": app.store.bots_worker.handle_docs,
        "web_app": app.store.bots_worker.handle_web_app,
        "text": app.store.bots_worker.handle_text,
    }
    async with message.process():
        handler = handlers[message.routing_key]
        upd = message.body.decode("utf-8")
        await handler(json.loads(upd))


async def listen_events(app: web.Application) -> None:
    """ Declare queue, message binding and start the listener. """
    connection = app["rabbitmq"]
    try:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=100)

        # Объявляем обменник
        exchange = await channel.declare_exchange(name="bot_exchange", type=aio_pika.ExchangeType.DIRECT, durable=True)

        # Объявляем и привязываем очереди к соответствующим маршрутизационным ключам
        cmds_queue = await channel.declare_queue(name="cmds_queue", durable=True)
        await cmds_queue.bind(exchange, routing_key="cmds")

        docs_queue = await channel.declare_queue(name="docs_queue", durable=True)
        await docs_queue.bind(exchange, routing_key="docs")

        web_app_queue = await channel.declare_queue(name="web_app_queue", durable=True)
        await web_app_queue.bind(exchange, routing_key="web_app")

        text_queue = await channel.declare_queue(name="text_queue", durable=True)
        await text_queue.bind(exchange, routing_key="text")

        # Запускаем асинхронное прослушивание для каждой из очередей
        await asyncio.gather(
            consume_messages(app, cmds_queue),
            consume_messages(app, docs_queue),
            consume_messages(app, web_app_queue),
            consume_messages(app, text_queue)
        )

    except asyncio.CancelledError as err:
        logger.info(f"Error while listening events: {err}")