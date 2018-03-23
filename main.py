import json
import logging
import os

import aiohttp
from discord.ext import commands

import core


class Bot(commands.AutoShardedBot):
    """A custom bot object that provides a configuration handler and an aiohttp ClientSession."""

    def __init__(self, *args, **kwargs):
        """In addition to everything supported by commands. Bot with some minor additions"""
        super().__init__(*args, **kwargs)
        self.config = {}
        self.session = aiohttp.ClientSession(loop=self.loop)

    def config_loading(self):
        """Load config from a JSON file."""

        with open("config.json") as file_object:
            config = json.load(file_object)
        if isinstance(config, dict):
            for key, value in config.items():
                self.config[key] = value


FORMAT = "%(asctime)-15s %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

bot = Bot(command_prefix="", pm_help=None,
          config_file="config.json", heatbeat_timeout=300.0)


if __name__ == "__main__":
    bot.config_loading()

    assert (isinstance(bot.config.get("discord_token"), str)
            ), "Invalid Bot token."
    assert (isinstance(bot.config.get("module_blacklist", []), list)
            ), "Blacklist must be a list."

    bot.description = bot.config.get("description", core.description)

    prefix = bot.config.get("prefix", "ema ")
    bot.command_prefix = commands.when_mentioned_or(*prefix)

    blacklist = bot.config.get("module_blacklist", [])

    # Automatically load all modules.
    for dirpath, dirnames, filenames in os.walk("extensions"):
        for filename in filenames:
            if filename.endswith(".py"):
                fullpath = os.path.join(dirpath, filename).split(os.sep)
                module = ".".join(fullpath)[:-3]
                if module in blacklist:  # Skip blacklisted modules.
                    continue
                try:
                    bot.load_extension(module)
                except Exception as error:
                    print(f"Unable to load {module}: {error}")
    bot.run(bot.config["discord_token"])
