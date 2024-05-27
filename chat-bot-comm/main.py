import os
import yaml
from dotenv import load_dotenv

from app.web.app import setup_app
from aiohttp.web import run_app

if __name__ == "__main__":

    try:
        dotenv_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), ".env"
        )
        load_dotenv(dotenv_path)
    except Exception:
        print("Problem with .env file")

    try:
        bot_token = os.environ['BOT_TOKEN']

        cfg_dict = {'bot': {'token': bot_token}}
        config_path=os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "config.yaml"
        )

        with open(config_path, 'w') as file:
            docs = yaml.dump(cfg_dict, file)

        run_app(setup_app(config_path))
    except KeyError:
        print("Environment variable does not exist")
