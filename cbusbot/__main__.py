"""Entrypoint: python -m cbusbot"""

import logging
import os
import sys

from dotenv import load_dotenv

from cbusbot.bot import CbusBot
from cbusbot.config import load_config


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    load_dotenv()
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        sys.exit("DISCORD_TOKEN is not set. Copy .env.example to .env and fill it in.")
    bot = CbusBot(load_config())
    bot.run(token, log_handler=None)


if __name__ == "__main__":
    main()
