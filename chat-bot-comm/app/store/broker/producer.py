import pika
import json
from logging import getLogger


logger = getLogger("PRODUCER")


def new_task(upd):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    body_ = json.dumps(upd)

    try:
        if "text" in upd["message"]:
            if upd["message"]["text"][0] == "/":
                channel.basic_publish(exchange='bot_exchange',
                                    routing_key='cmds',
                                    body=body_)
                logger.info("task was sended via 'cmds' routing_key")
            else:
                channel.basic_publish(exchange='bot_exchange',
                                      routing_key='text',
                                      body=body_)
                logger.info("task was sended via 'text' routing_key")

        elif "document" in upd["message"]:
            channel.basic_publish(exchange='bot_exchange',
                                routing_key='docs',
                                body=body_)
            logger.info("task was sended via 'docs' routing_key")

        elif "web_app_data" in upd["message"]:
            channel.basic_publish(exchange='bot_exchange',
                                  routing_key='web_app',
                                  body=body_)
            logger.info("task was sended via 'web_app' routing_key")

        logger.info(f" [x] Sent {body_}")
    except Exception as err:
        logger.info(f"Error while producing task: {err}")

    connection.close()
